import asyncio
import base64
import json
from typing import Dict, Optional, Any
from loguru import logger

from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from app.core.config import settings


class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.contexts: Dict[str, BrowserContext] = {}
        self.pages: Dict[str, Page] = {}
        self.cdp_sessions: Dict[str, Any] = {}
        self._frame_queues: Dict[str, asyncio.Queue] = {}
        self._screencast_tasks: Dict[str, asyncio.Task] = {}

    async def start(self):
        if self.playwright is None:
            self.playwright = await async_playwright().start()
        if self.browser is None:
            self.browser = await self.playwright.chromium.launch(
                headless=settings.BROWSER_HEADLESS,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                ],
            )
        logger.info("Playwright browser launched")

    async def create_session(self, session_id: str, start_url: Optional[str] = None):
        await self.start()
        context = await self.browser.new_context(
            viewport={"width": settings.BROWSER_VIEWPORT_WIDTH, "height": settings.BROWSER_VIEWPORT_HEIGHT},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="America/New_York",
        )
        page = await context.new_page()
        self.contexts[session_id] = context
        self.pages[session_id] = page
        self._frame_queues[session_id] = asyncio.Queue(maxsize=5)
        if start_url:
            try:
                await page.goto(start_url, wait_until="domcontentloaded", timeout=60000)
            except Exception as e:
                logger.warning(f"Goto failed: {e}")
        await self._start_screencast(session_id)
        return {"session_id": session_id, "url": page.url}

    async def _start_screencast(self, session_id: str):
        page = self.pages.get(session_id)
        if not page:
            return
        client = await page.context.new_cdp_session(page)
        self.cdp_sessions[session_id] = client

        async def on_frame(event):
            try:
                frame_data = event.get("data")
                if frame_data:
                    q = self._frame_queues.get(session_id)
                    if q and not q.full():
                        await q.put(frame_data)
            except Exception:
                pass

        client.on("Page.screencastFrame", on_frame)
        try:
            await client.send("Page.startScreencast", {
                "format": "jpeg",
                "quality": settings.CDP_SCREENCAST_QUALITY,
                "maxWidth": settings.BROWSER_VIEWPORT_WIDTH,
                "maxHeight": settings.BROWSER_VIEWPORT_HEIGHT,
                "everyNthFrame": 1,
            })
        except Exception as e:
            logger.warning(f"Screencast start failed: {e}")

    async def get_frame(self, session_id: str, timeout: float = 1.0):
        q = self._frame_queues.get(session_id)
        if not q:
            return None
        try:
            frame = await asyncio.wait_for(q.get(), timeout=timeout)
            return frame
        except asyncio.TimeoutError:
            return None

    async def input_click(self, session_id: str, x: int, y: int):
        page = self.pages.get(session_id)
        if not page:
            return
        await page.mouse.click(x, y)

    async def input_type(self, session_id: str, text: str):
        page = self.pages.get(session_id)
        if not page:
            return
        await page.keyboard.type(text)

    async def input_scroll(self, session_id: str, dx: int = 0, dy: int = 500):
        page = self.pages.get(session_id)
        if not page:
            return
        await page.mouse.wheel(dx, dy)

    async def navigate(self, session_id: str, url: str):
        page = self.pages.get(session_id)
        if not page:
            return
        await page.goto(url, wait_until="domcontentloaded")

    async def get_current_url(self, session_id: str):
        page = self.pages.get(session_id)
        if not page:
            return None
        return page.url

    async def detect_state(self, session_id: str):
        page = self.pages.get(session_id)
        if not page:
            return {"login": False, "captcha": False, "url": None}
        try:
            url = page.url
            content = await page.content()
            content_low = content.lower()
            login_ind = any(k in content_low for k in ["type=\"password\"", "sign in", "log in", "login"])
            captcha_ind = any(k in content_low for k in ["recaptcha", "hcaptcha", "turnstile", "verify you are human", "cloudflare"])
            return {"login": login_ind and ("password" in content_low), "captcha": captcha_ind, "url": url}
        except Exception:
            return {"login": False, "captcha": False, "url": None}

    async def close_session(self, session_id: str):
        try:
            page = self.pages.pop(session_id, None)
            ctx = self.contexts.pop(session_id, None)
            if page and not page.is_closed():
                await page.close()
            if ctx:
                await ctx.close()
        except Exception as e:
            logger.warning(f"Close session error: {e}")



browser_manager = BrowserManager()
