from flask import render_template
from flask_login import login_required
from flask_babel import _
from app import db
from app.stats import bp
from app.models import Request

@bp.route('/total_hits')
@login_required
def total_hits():
	result = db.engine.execute("select distinct path, count(path) from request group by path")
	path=[]
	hits=[]
	total = Request.query.all()
	for row in result:
		path.append(row['path'])
		hits.append(row['count'])
	maximum = max(hits)
	return render_template('stats/total_hits.html', title=_('Total page visits'), 
			paths=path, hits=hits, total=len(total), max=maximum)