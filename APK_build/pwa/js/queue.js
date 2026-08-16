/** Простая асинхронная FIFO-очередь — замена asyncio.Queue из Python-версии. */
export class AsyncQueue {
  constructor() {
    this._items = [];
    this._waiters = [];
  }

  put(item) {
    if (this._waiters.length) {
      this._waiters.shift()(item);
    } else {
      this._items.push(item);
    }
  }

  get empty() {
    return this._items.length === 0;
  }

  /** Забрать один элемент без ожидания (кидает, если пусто) — аналог get_nowait(). */
  getNowait() {
    if (!this._items.length) throw new Error("queue empty");
    return this._items.shift();
  }

  /** Забрать элемент, ждать до timeoutMs (или бесконечно, если не задан). null при таймауте. */
  async get(timeoutMs) {
    if (this._items.length) return this._items.shift();
    return new Promise((resolve) => {
      let done = false;
      const timer = timeoutMs != null
        ? setTimeout(() => {
            if (done) return;
            done = true;
            const idx = this._waiters.indexOf(waiter);
            if (idx >= 0) this._waiters.splice(idx, 1);
            resolve(null);
          }, timeoutMs)
        : null;
      const waiter = (item) => {
        if (done) return;
        done = true;
        if (timer) clearTimeout(timer);
        resolve(item);
      };
      this._waiters.push(waiter);
    });
  }

  clear() {
    this._items.length = 0;
  }
}
