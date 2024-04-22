import thriftpy
from thriftpy.rpc import make_client
from thriftpy.thrift import TException

calculator_thrift = thriftpy.load(
    '../calculator.thrift', module_name='calculator_thrift')
Calculator = calculator_thrift.CalculatorService


def main():
    try:
        # Instantiate a synchronous client
        client = make_client(Calculator, '127.0.0.1', 9090)

        arg1 = 3
        arg2 = 5

        # Use the stub method to call the RPC Server. This is a blocking call.
        result = client.multiply(arg1, arg2)

        # after receiving the result the call above will un-block
        # print the result
        print('%d * %d = %d' % (arg1, arg2, result))
    except TException as e:
        print(e)


if __name__ == '__main__':
    main()
