var Deque = require("double-ended-queue");

export const FetchQueueService = {
  enqueue: function(url) {
    this.queue.enqueue(url);
  },
  dequeue: function() {
    return this.queue.dequeue();
  },
  queue: new Deque()
};
