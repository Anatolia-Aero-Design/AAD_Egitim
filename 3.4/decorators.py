import functools

def service_caller(func):
    """
    A simpler decorator. It expects the decorated function to return:
    (client_object, request_object, step_name)
    """

    @functools.wraps(func) # Copies metadata from the given func (__str__, __doc__ etc.)
    def wrapper(self, *args, **kwargs):
        # 1. Run the function FIRST to get the client and request
        # We don't need to wait for the service to create a Request object!
        client, request = func(self, *args, **kwargs)
        
        # 2. NOW we wait for the client we just received
        self.get_logger().info(f'Waiting for service: {client.srv_name}...')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(f'{client.srv_name} not available, waiting...')

        future = client.call_async(request)
        
        # 4. Attach Callback
        future.add_done_callback(lambda f: self.on_step_complete(f))
        
    return wrapper