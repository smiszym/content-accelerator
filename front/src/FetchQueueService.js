var Deque = require("double-ended-queue");

export const FetchQueueService = {
  insertWithPriority(url) {
    // Called when the user tries to access a URL that is not yet in cache;
    // it will be fetched with highest priority.
    this.queue.insertFront(url);
  },
  enqueue: function(url) {
    this.queue.enqueue(url);
  },
  dequeue: function() {
    return this.queue.dequeue();
  },
  queue: new Deque()
};
