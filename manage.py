import argparse
import app
import parser
from validate import validate_date


#
ps = argparse.ArgumentParser(description='scraping airbnb and booking')
ps.add_argument(
    'destination',
    metavar='DESTINATION',
    type=str,
    nargs=None,
    help='destination')
ps.add_argument(
    'checkin',
    metavar='YYYY-MM-DD',
    type=str,
    nargs=None,
    help='checkin date: YYYY-MM-DD')
ps.add_argument(
    'checkout',
    metavar='YYYY-MM-DD',
    type=str,
    nargs=None,
    help='checkout date: YYYY-MM-DD')
args = ps.parse_args()


if __name__ == "__main__":
    validate_date(args.checkin)
    validate_date(args.checkout)
    app.run(args.destination, args.checkin, args.checkout)
    parser.run()
