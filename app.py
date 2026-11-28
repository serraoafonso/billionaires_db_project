import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

from flask import Flask, abort, render_template, request
import db

APP = Flask(__name__)


# ===========================================================================
# Página inicial (/)
# ===========================================================================

@APP.route('/')
def index():
    stats = {
        'billionaires': db.execute('SELECT COUNT(*) AS n FROM billionaires').fetchone()['n'],
        'countries': db.execute('SELECT COUNT(*) AS n FROM countries').fetchone()['n'],
        'industries': db.execute('SELECT COUNT(*) AS n FROM industries').fetchone()['n'],
        'organizations': db.execute('SELECT COUNT(*) AS n FROM organizations').fetchone()['n'],
    }
    return render_template('index.html', stats=stats)


# ===========================================================================
# Entidade: Bilionários (/billionaires e /billionaires/<id>)
# ===========================================================================

@APP.route('/billionaires')
def list_billionaires():
    billionaires = db.execute("""
        SELECT b.billionaire_id, b.rank, b.full_name, b.net_worth_million,
               b.age, b.self_made,
               c.country_id, c.name AS country_name,
               i.industry_id, i.name AS industry_name,
               o.organization_id, o.name AS organization_name
        FROM billionaires b
        JOIN countries c ON b.citizenship_country_id = c.country_id
        JOIN industries i ON b.industry_id = i.industry_id
        LEFT JOIN organizations o ON b.organization_id = o.organization_id
        ORDER BY b.rank ASC
    """).fetchall()
    return render_template('billionaires.html', billionaires=billionaires)


@APP.route('/billionaires/<int:id>')
def get_billionaire(id):
    billionaire = db.execute("""
        SELECT b.*,
               cc.name AS citizenship_name,
               rc.name AS residence_name,
               i.name AS industry_name,
               o.name AS organization_name
        FROM billionaires b
        JOIN countries cc ON b.citizenship_country_id = cc.country_id
        JOIN countries rc ON b.residence_country_id = rc.country_id
        JOIN industries i ON b.industry_id = i.industry_id
        LEFT JOIN organizations o ON b.organization_id = o.organization_id
        WHERE b.billionaire_id = ?
    """, [id]).fetchone()

    if billionaire is None:
        abort(404)

    return render_template('billionaire.html', b=billionaire)


# ===========================================================================
# Entidade: Países (/countries e /countries/<id>)
# ===========================================================================

@APP.route('/countries')
def list_countries():
    countries = db.execute("""
        SELECT c.country_id, c.name, c.region, c.gdp_billion_usd, c.population,
               COUNT(b.billionaire_id) AS billionaire_count
        FROM countries c
        LEFT JOIN billionaires b ON b.citizenship_country_id = c.country_id
        GROUP BY c.country_id
        ORDER BY billionaire_count DESC, c.name ASC
    """).fetchall()
    return render_template('countries.html', countries=countries)


@APP.route('/countries/<int:id>')
def get_country(id):
    country = db.execute(
        'SELECT * FROM countries WHERE country_id = ?',
        [id]
    ).fetchone()

    if country is None:
        abort(404)

    billionaires = db.execute("""
        SELECT b.billionaire_id, b.rank, b.full_name, b.net_worth_million,
               i.industry_id, i.name AS industry_name
        FROM billionaires b
        JOIN industries i ON b.industry_id = i.industry_id
        WHERE b.citizenship_country_id = ?
        ORDER BY b.net_worth_million DESC
    """, [id]).fetchall()

    organizations = db.execute("""
        SELECT o.organization_id, o.name, i.industry_id, i.name AS industry_name
        FROM organizations o
        JOIN industries i ON o.industry_id = i.industry_id
        WHERE o.hq_country_id = ?
        ORDER BY o.name ASC
    """, [id]).fetchall()

    return render_template(
        'country.html',
        country=country,
        billionaires=billionaires,
        organizations=organizations,
    )


# ===========================================================================
# Entidade: Indústrias (/industries e /industries/<id>)
# ===========================================================================

@APP.route('/industries')
def list_industries():
    industries = db.execute("""
        SELECT i.industry_id, i.name,
               COUNT(b.billionaire_id) AS billionaire_count,
               COALESCE(SUM(b.net_worth_million), 0) AS total_worth
        FROM industries i
        LEFT JOIN billionaires b ON b.industry_id = i.industry_id
        GROUP BY i.industry_id
        ORDER BY total_worth DESC, i.name ASC
    """).fetchall()
    return render_template('industries.html', industries=industries)


@APP.route('/industries/<int:id>')
def get_industry(id):
    industry = db.execute(
        'SELECT * FROM industries WHERE industry_id = ?',
        [id]
    ).fetchone()

    if industry is None:
        abort(404)

    billionaires = db.execute("""
        SELECT b.billionaire_id, b.rank, b.full_name, b.net_worth_million,
               c.country_id, c.name AS country_name
        FROM billionaires b
        JOIN countries c ON b.citizenship_country_id = c.country_id
        WHERE b.industry_id = ?
        ORDER BY b.net_worth_million DESC
    """, [id]).fetchall()

    organizations = db.execute("""
        SELECT o.organization_id, o.name, c.country_id, c.name AS country_name
        FROM organizations o
        JOIN countries c ON o.hq_country_id = c.country_id
        WHERE o.industry_id = ?
        ORDER BY o.name ASC
    """, [id]).fetchall()

    return render_template(
        'industry.html',
        industry=industry,
        billionaires=billionaires,
        organizations=organizations,
    )


# ===========================================================================
# Entidade: Organizações (/organizations e /organizations/<id>)
# ===========================================================================

@APP.route('/organizations')
def list_organizations():
    organizations = db.execute("""
        SELECT o.organization_id, o.name,
               i.industry_id, i.name AS industry_name,
               c.country_id, c.name AS country_name
        FROM organizations o
        JOIN industries i ON o.industry_id = i.industry_id
        JOIN countries c ON o.hq_country_id = c.country_id
        ORDER BY o.name ASC
    """).fetchall()
    return render_template('organizations.html', organizations=organizations)


@APP.route('/organizations/<int:id>')
def get_organization(id):
    organization = db.execute("""
        SELECT o.organization_id, o.name,
               i.industry_id, i.name AS industry_name,
               c.country_id, c.name AS country_name
        FROM organizations o
        JOIN industries i ON o.industry_id = i.industry_id
        JOIN countries c ON o.hq_country_id = c.country_id
        WHERE o.organization_id = ?
    """, [id]).fetchone()

    if organization is None:
        abort(404)

    billionaires = db.execute("""
        SELECT b.billionaire_id, b.rank, b.full_name, b.net_worth_million,
               c.country_id, c.name AS country_name
        FROM billionaires b
        JOIN countries c ON b.citizenship_country_id = c.country_id
        WHERE b.organization_id = ?
        ORDER BY b.net_worth_million DESC
    """, [id]).fetchall()

    return render_template(
        'organization.html',
        organization=organization,
        billionaires=billionaires,
    )


# ===========================================================================
# As 10 Interrogações SQL (/queries/1 até /queries/10)
# TODO: Substituir pelas 10 interrogações entregues pela Pessoa 3 (sql/queries.sql)
# ===========================================================================

@APP.route('/queries/1')
def query1():
    min_worth = request.args.get('min_worth', default=0, type=int)
    rows = db.execute("""
        SELECT b.billionaire_id, b.rank, b.full_name, b.net_worth_million,
               c.country_id, c.name AS country_name,
               i.industry_id, i.name AS industry_name
        FROM billionaires b
        JOIN countries c ON b.citizenship_country_id = c.country_id
        JOIN industries i ON b.industry_id = i.industry_id
        WHERE b.net_worth_million >= ?
        ORDER BY b.net_worth_million DESC
    """, [min_worth]).fetchall()
    return render_template('query1.html', rows=rows, min_worth=min_worth)


@APP.route('/queries/2')
def query2():
    rows = db.execute("""
        SELECT c.country_id, c.name AS country_name, c.region,
               COUNT(b.billionaire_id) AS total_billionaires,
               SUM(b.net_worth_million) AS total_worth,
               ROUND(AVG(b.net_worth_million), 1) AS avg_worth
        FROM countries c
        JOIN billionaires b ON b.citizenship_country_id = c.country_id
        GROUP BY c.country_id, c.name, c.region
        ORDER BY total_worth DESC
    """).fetchall()
    return render_template('query2.html', rows=rows)


@APP.route('/queries/3')
def query3():
    rows = db.execute("""
        SELECT b.billionaire_id, b.full_name, b.net_worth_million,
               i.industry_id, i.name AS industry_name,
               ROUND((
                   SELECT AVG(b2.net_worth_million)
                   FROM billionaires b2
                   WHERE b2.industry_id = b.industry_id
               ), 1) AS industry_avg
        FROM billionaires b
        JOIN industries i ON b.industry_id = i.industry_id
        WHERE b.self_made = 1
          AND b.net_worth_million > (
              SELECT AVG(b2.net_worth_million)
              FROM billionaires b2
              WHERE b2.industry_id = b.industry_id
          )
        ORDER BY b.net_worth_million DESC
    """).fetchall()
    return render_template('query3.html', rows=rows)


# Rotas provisórias para Q4..Q10 até a Pessoa 3 entregar sql/queries.sql
@APP.route('/queries/<int:query_id>')
def query_todo(query_id):
    if query_id < 4 or query_id > 10:
        abort(404)
    return render_template('query_todo.html', query_id=query_id)


# ===========================================================================
# Página de erro 404
# ===========================================================================

@APP.errorhandler(404)
def page_not_found(_error):
    return render_template('404.html'), 404
