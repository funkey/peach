import tqdm
from .server_observer import ServerObserver


class CLMonitor(ServerObserver):

    def __init__(self, server):
        super().__init__(server)
        self.progresses = {}

    def on_acquire_block(self, task_id, task_state):
        self._update_state(task_id, task_state)

    def on_release_block(self, task_id, task_state):
        self._update_state(task_id, task_state)

    def on_task_done(self, task_id):
        print(f"Task {task_id} completed")

    def _update_state(self, task_id, task_state):

        if task_id not in self.progresses:
            total = task_state.total_block_count
            self.progresses[task_id] = tqdm.tqdm(
                total=total,
                desc=task_id,
                unit='blocks',
                leave=False)

        completed = task_state.completed_count
        delta = completed - self.progresses[task_id].n
        if delta > 0:
            self.progresses[task_id].update(delta)
