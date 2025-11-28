from helper import Helper

class Stepper(Helper):
    def __init__(self, get_logger, end_order):
        super().__init__(get_logger, end_order)

    def _run_next_step(self):
        """Görev dizisindeki bir sonraki adimi yürütür."""
        for i, (step_func, step_name) in enumerate(self.steps):
            self.get_logger().info(f"--- Adim {i + 1}/{len(self.steps)} yürütülüyor ---")
            self.get_logger().info(f"Adim Açiklamasi: {step_name}")

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
            self.get_logger().info("Adimlar tamamlandi!")
        except Exception as e:
            self.get_logger().error(f"Adim sirasinda hata oluştu: {e}")
    