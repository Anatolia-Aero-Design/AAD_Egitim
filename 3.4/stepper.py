class Stepper:
    def __init__(self, logger, steps):
        self.logger = logger
        self.assign_steps(steps)

    def _run_next_step(self):
        """Görev dizisindeki bir sonraki adimi yürütür."""
        for i, (step_func, step_name) in enumerate(self.steps):
            self.logger.info(f"--- Adim {i + 1}/{len(self.steps)} yürütülüyor ---")
            self.logger.info(f"Adim Açiklamasi: {step_name}")

            step_func()
            yield

    def assign_steps(self, steps):
        self._iterator = self._run_next_step()
        self.steps = steps

    def start_mission_flow(self, timer):
        timer.cancel()
        self.step()

    def step(self):
        """Her çağrida, generator'i bir adim ilerletir."""
        try:
            next(self._iterator) 
        except StopIteration:
            self.logger.info("Adimlar tamamlandi!")
        except Exception as e:
            self.logger.error(f"Adim sirasinda hata oluştu: {e}")

    def on_step_complete(self, future):
        self.step()

    