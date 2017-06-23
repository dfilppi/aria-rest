from flask import Flask, render_template
from aria.exceptions import AriaException

version_id = "0.1"
route_base = "/api/" + version_id + "/"
app = Flask("onap-aria-rest")

@app.route("/")
def index():
  return render_template('index.html')


@app.route(route_base + "templates/", methods = ['GET'])
def list_templates():

@app.route(route_base + "templates/<template_id>", methods = ['POST'])
def install_template( template_id ):

  # GET CSAR FROM SDC

  # DEPLOY CSAR

  # UPDATE A&AI?

  return "template {} instantiated"

@app.route(route_base + "templates/<template_id>", methods = ['DELETE'])
def delete_template( template_id ):

  # RUN UNINSTALL

  # DELETE TEMPLATE

  # UPDATE A&AI?

  return "template {} deleted"

if __name__ == "__main__":
  app.run()
