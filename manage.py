import argparse, app, parser
from validate import validate_date


parser = argparse.ArgumentParser(description='scraping airbnb and booking')
parser.add_argument('destination', metavar='DESTINATION', type=str, nargs=None, help='destination')
parser.add_argument('checkin', metavar='YYYY-MM-DD', type=str, nargs=None, help='checkin date: YYYY-MM-DD')
parser.add_argument('checkout', metavar='YYYY-MM-DD', type=str, nargs=None, help='checkout date: YYYY-MM-DD')
args = parser.parse_args()


if __name__ == "__main__":
    validate_date(args.checkin)
    validate_date(args.checkout)
    app.run(args.destination, args.checkin, args.checkout)
    parser.run()
