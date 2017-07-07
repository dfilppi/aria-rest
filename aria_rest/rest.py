import sys
from flask import Flask, render_template, request
from aria.exceptions import AriaException
import util

version_id = "0.1"
route_base = "/api/" + version_id + "/"
app = Flask("onap-aria-rest")

def main():
  app.run()

@app.route("/")
def index():
  return render_template('index.html')


###
### TEMPLATES
###

# add template
@app.route(route_base + "templates/<template_id>", methods = ['POST'])
def install_template( template_id ):
  
  return "template {} instantiated"

# validate template
@app.route(route_base + "templates/validate", methods = ['POST'])
def validate_template():
  raise AriaException("not implemented")

# delete template
@app.route(route_base + "templates/<template_id>", methods = ['DELETE'])
def delete_template( template_id ):
  raise AriaException("not implemented")

# list nodes
@app.route(route_base + "templates/<template_id>"/nodes", methods = ['GET'])
def list_nodes(template_id):
  raise AriaException("not implemented")
  
@app.route(route_base + "templates/<template_id>"/nodes/<node_id>", methods = ['GET'])
def get_node(template_id, node_id):
  raise AriaException("not implemented")

###
### SERVICES
###

# list services
@app.route(route_base + "services", methods = ['GET'])
def list_services():
  raise AriaException("not implemented")

# show service
@app.route(route_base + "services/<service_name>", methods = ['GET'])
def show_service(service_name):
  raise AriaException("not implemented")

# get service outputs
@app.route(route_base + "services/<service_name>/outputs", methods = ['GET'])
def show_service(service_name):
  raise AriaException("not implemented")

# get service inputs
@app.route(route_base + "services/<service_name>/inputs", methods = ['GET'])
def show_service(service_name):
  raise AriaException("not implemented")

# create service
@app.route(route_base + "services/<service_name>", methods = ['POST'])
def create_service(service_name):
  raise AriaException("not implemented")

# delete service
@app.route(route_base + "services/<service_name>", methods = ['DELETE'])
def delete_service(service_name):
  raise AriaException("not implemented")

###
### WORKFLOWS
###

# list workflows
@app.route(route_base + "services/<service_name>/workflows", methods = ['GET'])
def list_workflows(service_name):
  raise AriaException("not implemented")

# show workflow
@app.route(route_base + "services/<service_name>/workflow/<workflow_name>", methods = ['GET'])
def show_workflows(service_name, workflow_name):
  raise AriaException("not implemented")

###
### EXECUTIONS
###

# list executions
@app.route(route_base + "executions", methods = ['GET'])
def list_executions():
  raise AriaException("not implemented")

# show execution
@app.route(route_base + "executions/<execution_id>", methods = ['GET'])
def show_execution(execution_id):
  raise AriaException("not implemented")

# start execution
@app.route(route_base + "executions/<service_name>/<workflow_name>", methods = ['POST'])
def show_execution(service_name, workflow_name):
  raise AriaException("not implemented")

## resume execution
@app.route(route_base + "executions/<execution_id>", methods = ['POST'])
def resume_execution(execution_id):
  raise AriaException("not implemented")

## cancel execution
@app.route(route_base + "executions/<execution_id>", methods = ['DELETE'])
def cancel_execution(execution_id):
  raise AriaException("not implemented")


if __name__ == "__main__":
  app.run()

