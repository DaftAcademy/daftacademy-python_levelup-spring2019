import time

def my_timer(fn):
	def wrapper(*args, **kwargs):
		start = time.perf_counter_ns()
		result = fn(*args, **kwargs)
		end = time.perf_counter_ns()
		delta = end - start
		print(f'{fn.__name__} elapsed {delta} nanoseconds')
		return result
	return wrapper


@my_timer
def fixed_sleep():
	time.sleep(3)
	return 'wstalem'


@my_timer
def mutable_sleep(jak_dlugo=2):
	time.sleep(jak_dlugo)
	return f'spalem {jak_dlugo}'


if __name__ == '__main__':
	val = fixed_sleep()
	print(val)
	val = mutable_sleep(2)
	print(val)
