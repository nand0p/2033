from utils import html, yf, disk
from flask import Flask
import os


app = Flask(__name__)
stocks = []
app.config['STOCKS'] = os.environ.get('STOCKS')
stocks = sorted(app.config['STOCKS'].strip('\"').upper().split())
avg_periods = [ 9, 21, 50, 75, 100, 200, 365, 500 ]
period = '5y'
interval = '1d'
minimum_score = 25
data_dir='./data/'


@app.route('/')
def x2030():
  h = ''
  h += html.header(stocks)
      
  scores = {}
  for stock in stocks:
    scores[stock] = 1
    df = yf.load_or_get_data(stock, period, interval)
    current = yf.find_current_price(df)
    h += '<tr><td width=200>'
    h += html.stock_info(stock)
    h += '</td><td>'
    h += html.generate_price_chart(stock, df)
    h += '</td><td width=200>'
    h, scores[stock] = html.calculate_high_low(stock, df, current, h, scores[stock], avg_periods)
    h, scores[stock] = html.calculate_averages(stock, df, current, h, scores[stock], avg_periods)
    color = yf.get_score_color(scores[stock])
    h += '<hr><table width=100%><tr><td bgcolor=' + color + '>'
    h += '<p><br><p><center>Score: ' + str(scores[stock])
    h += '<p><br><p></td></tr></table></td></tr>'

  h += html.footer(scores, minimum_score)

  disk.save_scores(scores, data_dir)

  return h


@app.route('/test')
def test():
  return 'success'


if __name__ == "__main__":
  app.run(debug=True, passthrough_errors=True)
