import pf
import time
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
filter = pf.PacketFilter()


@app.route("/")
def index():
    status = filter.get_status()
    tables = filter.get_tables()
    rules = filter.get_ruleset()
    return render_template("index.html", tables=tables,
                            rules=rules, status=status)


@app.route("/disable")
def disable():
    filter.disable()
    return redirect(url_for('index'))


@app.route("/enable")
def enable():
    filter.enable()
    return redirect(url_for('index'))


@app.route("/rules/delete/<id>")
def delete_rule(id):
    new_rs = filter.get_ruleset()
    new_rs.remove(int(id))
    filter.load_ruleset(new_rs, '')
    return redirect(url_for('index'))


@app.route("/tables/<name>")
def tables(name):
    addrs = filter.get_addrs(pf.PFTable(name))
    stats = filter.get_tstats(pf.PFTable(name))
    return render_template("tables.html", addrs=addrs, name=name, stats=stats)


@app.route('/tables/add/<name>', methods=['POST'])
def add_address_to_table(name):
    filter.add_addrs(name, request.form['address'])
    return redirect(url_for('tables', name=name))


@app.route('/tables/clear_stats/<name>')
def clear_stats(name):
    filter.clear_tstats(pf.PFTable(name))
    return redirect(url_for('tables', name=name))


@app.template_filter('format_time')
def format_time(timestamp):
    return time.ctime(timestamp)


@app.template_filter('mbyte')
def mbyte(bytes):
    return round(bytes / 1024.0 / 1024.0, 2)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
