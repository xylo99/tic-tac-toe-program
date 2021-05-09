from client.tttc import Client
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Tic Tac Toe client! In order for the client to start first, "
                                                 "only pass the flag '--client-start' as an argument to the "
                                                 "program. To specify the IP, pass --ip A.B.C.D to the program.")
    parser.add_argument('--ip', help="IP address of the server. Use the A.B.C.D format.")
    parser.add_argument('--client_start', action="store_true", help="Client will start first if this argument is"
                                                                    "passed to the program.")
    args = parser.parse_args()

    return args.ip, bytes(args.client_start)


if __name__ == "__main__":
    ip, cs = parse_args()
    cli = Client(ip, cs)
    cli.run_client()
