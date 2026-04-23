# tests/aliases/test_asyncio.py
# B-037 stdlib aliases — asyncio module tests
#
# Tests run actual coroutines where possible, keeping them short and self-
# contained. اتزامن.شغل() is the entry point for every async test.

import asyncio
import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def اتزامن():
    """Return a ModuleProxy wrapping `asyncio`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("اتزامن", None, None)
    assert spec is not None, "AliasFinder did not find 'اتزامن'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestAsyncioProxy:
    # ── Core function aliases ─────────────────────────────────────────────────

    def test_run_alias(self, اتزامن):
        """شغل maps to asyncio.run."""
        assert اتزامن.شغل is asyncio.run

    def test_sleep_alias(self, اتزامن):
        """تريث maps to asyncio.sleep."""
        assert اتزامن.تريث is asyncio.sleep

    def test_gather_alias(self, اتزامن):
        """اجمع_مهام maps to asyncio.gather."""
        assert اتزامن.اجمع_مهام is asyncio.gather

    def test_wait_alias(self, اتزامن):
        """انتظر maps to asyncio.wait."""
        assert اتزامن.انتظر is asyncio.wait

    def test_wait_for_alias(self, اتزامن):
        """انتظر_من_اجل maps to asyncio.wait_for."""
        assert اتزامن.انتظر_من_اجل is asyncio.wait_for

    def test_shield_alias(self, اتزامن):
        """درع maps to asyncio.shield."""
        assert اتزامن.درع is asyncio.shield

    def test_as_completed_alias(self, اتزامن):
        """اكمل_ما_ينتهي maps to asyncio.as_completed."""
        assert اتزامن.اكمل_ما_ينتهي is asyncio.as_completed

    def test_create_task_alias(self, اتزامن):
        """انشئ_مهمه maps to asyncio.create_task."""
        assert اتزامن.انشئ_مهمه is asyncio.create_task

    def test_current_task_alias(self, اتزامن):
        """مهمه_حاليه maps to asyncio.current_task."""
        assert اتزامن.مهمه_حاليه is asyncio.current_task

    def test_all_tasks_alias(self, اتزامن):
        """كل_المهام maps to asyncio.all_tasks."""
        assert اتزامن.كل_المهام is asyncio.all_tasks

    def test_to_thread_alias(self, اتزامن):
        """في_خيط maps to asyncio.to_thread."""
        assert اتزامن.في_خيط is asyncio.to_thread

    # ── Class aliases ─────────────────────────────────────────────────────────

    def test_task_class_alias(self, اتزامن):
        """مهمه maps to asyncio.Task."""
        assert اتزامن.مهمه is asyncio.Task

    def test_future_class_alias(self, اتزامن):
        """مستقبل maps to asyncio.Future."""
        assert اتزامن.مستقبل is asyncio.Future

    def test_task_group_alias(self, اتزامن):
        """مجموعة_مهام maps to asyncio.TaskGroup."""
        assert اتزامن.مجموعة_مهام is asyncio.TaskGroup

    def test_event_loop_alias(self, اتزامن):
        """حلقه_احداث maps to asyncio.EventLoop."""
        assert اتزامن.حلقه_احداث is asyncio.EventLoop

    def test_lock_alias(self, اتزامن):
        """قفل maps to asyncio.Lock."""
        assert اتزامن.قفل is asyncio.Lock

    def test_event_alias(self, اتزامن):
        """حدث maps to asyncio.Event."""
        assert اتزامن.حدث is asyncio.Event

    def test_semaphore_alias(self, اتزامن):
        """سيمافور maps to asyncio.Semaphore."""
        assert اتزامن.سيمافور is asyncio.Semaphore

    def test_queue_alias(self, اتزامن):
        """صف_مهام maps to asyncio.Queue."""
        assert اتزامن.صف_مهام is asyncio.Queue

    def test_timeout_alias(self, اتزامن):
        """مهله maps to asyncio.timeout."""
        assert اتزامن.مهله is asyncio.timeout

    # ── Exception aliases ─────────────────────────────────────────────────────

    def test_cancelled_error_alias(self, اتزامن):
        """خطا_الغاء maps to asyncio.CancelledError."""
        assert اتزامن.خطا_الغاء is asyncio.CancelledError

    def test_timeout_error_alias(self, اتزامن):
        """خطا_مهله maps to asyncio.TimeoutError."""
        assert اتزامن.خطا_مهله is asyncio.TimeoutError

    # ── Coroutine check aliases ───────────────────────────────────────────────

    def test_iscoroutine_alias(self, اتزامن):
        """هل_كوروتين maps to asyncio.iscoroutine."""
        assert اتزامن.هل_كوروتين is asyncio.iscoroutine

    def test_iscoroutinefunction_alias(self, اتزامن):
        """هل_دالة_كوروتين maps to asyncio.iscoroutinefunction."""
        assert اتزامن.هل_دالة_كوروتين is asyncio.iscoroutinefunction

    # ── Event loop function aliases ───────────────────────────────────────────

    def test_get_event_loop_alias(self, اتزامن):
        """احضر_حلقه_احداث maps to asyncio.get_event_loop."""
        assert اتزامن.احضر_حلقه_احداث is asyncio.get_event_loop

    def test_get_running_loop_alias(self, اتزامن):
        """احضر_حلقه_عامله maps to asyncio.get_running_loop."""
        assert اتزامن.احضر_حلقه_عامله is asyncio.get_running_loop

    def test_new_event_loop_alias(self, اتزامن):
        """حلقه_احداث_جديده maps to asyncio.new_event_loop."""
        assert اتزامن.حلقه_احداث_جديده is asyncio.new_event_loop

    # ── Functional async tests ────────────────────────────────────────────────

    def test_run_simple_coroutine(self, اتزامن):
        """شغل executes a simple coroutine and returns its result."""

        async def كوروتين_بسيط():
            return 42

        result = اتزامن.شغل(كوروتين_بسيط())
        assert result == 42

    def test_sleep_zero(self, اتزامن):
        """تريث(0) yields control without blocking; completes immediately."""

        async def main():
            await asyncio.sleep(0)
            return "done"

        assert اتزامن.شغل(main()) == "done"

    def test_gather_multiple(self, اتزامن):
        """اجمع_مهام awaits multiple coroutines and returns all results."""

        async def value(n):
            return n * 2

        async def main():
            return await asyncio.gather(value(1), value(2), value(3))

        results = اتزامن.شغل(main())
        assert results == [2, 4, 6]

    def test_lock_prevents_concurrent_access(self, اتزامن):
        """قفل (Lock) prevents concurrent modification of shared state."""

        async def main():
            lock = asyncio.Lock()
            shared = []

            async def writer(val):
                async with lock:
                    shared.append(val)

            await asyncio.gather(writer(1), writer(2), writer(3))
            return sorted(shared)

        assert اتزامن.شغل(main()) == [1, 2, 3]

    def test_event_set_and_wait(self, اتزامن):
        """حدث (Event) signals between coroutines."""

        async def main():
            event = asyncio.Event()
            results = []

            async def setter():
                event.set()
                results.append("set")

            async def waiter():
                await event.wait()
                results.append("waited")

            await asyncio.gather(setter(), waiter())
            return results

        result = اتزامن.شغل(main())
        assert "set" in result
        assert "waited" in result

    def test_queue_put_get(self, اتزامن):
        """صف_مهام (Queue) supports put and get operations."""

        async def main():
            q = asyncio.Queue()
            await q.put("مرحبا")
            await q.put("عالم")
            a = await q.get()
            b = await q.get()
            return [a, b]

        assert اتزامن.شغل(main()) == ["مرحبا", "عالم"]

    def test_iscoroutinefunction_check(self, اتزامن):
        """هل_دالة_كوروتين returns True for async def functions."""

        async def my_coro():
            pass

        assert اتزامن.هل_دالة_كوروتين(my_coro)
        assert not اتزامن.هل_دالة_كوروتين(lambda: None)

    def test_wait_for_timeout(self, اتزامن):
        """انتظر_من_اجل raises TimeoutError when coroutine exceeds timeout."""

        async def slow():
            await asyncio.sleep(10)

        async def main():
            with pytest.raises(asyncio.TimeoutError):
                await asyncio.wait_for(slow(), timeout=0.001)

        اتزامن.شغل(main())
