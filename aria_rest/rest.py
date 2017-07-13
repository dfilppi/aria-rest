import sys, os
from flask import Flask, render_template, request, jsonify
from flask_autodoc.autodoc import Autodoc
from aria import install_aria_extensions
from aria.cli.core import aria
from aria.exceptions import AriaException
from aria.core import Core
from aria.cli import service_template_utils
from aria.storage import exceptions as storage_exceptions
from aria.utils import threading
from aria.orchestrator.workflow_runner import WorkflowRunner
from aria.orchestrator.workflows.executor.dry import DryExecutor
import json
import util

version_id = "0.1"
route_base = "/api/" + version_id + "/"
app = Flask("onap-aria-rest")
auto = Autodoc(app)

def main():
  install_aria_extensions()
  app.run()

@app.route("/")
@app.route("/api")
@app.route("/docs")
def index():
  return auto.html()


###
### TEMPLATES
###

# add template
@app.route(route_base + "templates/<template_name>", methods = ['PUT'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_resource_storage
@aria.pass_plugin_manager
@aria.pass_logger
def install_template( template_name, model_storage, resource_storage,
                      plugin_manager, logger):
  body = request.json

  # Check body
  if "service-template-path" in body:
    service_template_path = body["service-template-path"]
  else:
    return "request body missing service-template-path",501

  if "service-template-filename" in body:
    service_template_filename = body["service-template-filename"]
  else:
    service_template_filename = "service-template.yaml"

  service_template_path = service_template_utils.get(service_template_path,
                                                     service_template_filename)
  core = Core(model_storage, resource_storage, plugin_manager)

  try:
    core.create_service_template(service_template_path,
                                 os.path.dirname(service_template_path),
                                 template_name)
  except storage_exceptions.StorageError as e:
    utils.check_overriding_storage_exceptions(e, 'service template', template_name)
  except Exception as e:
    return e.message, 500

  return "service template installed", 200

# validate template
@app.route(route_base + "templates", methods = ['POST'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_resource_storage
@aria.pass_plugin_manager
@aria.pass_logger
def validate_template( model_storage, resource_storage, plugin_manager, logger):
  body = request.json
  
  # Check body
  if "service-template-path" in body:
    service_template_path = body["service-template-path"]
  else:
    return "request body missing service-template-path",501
  if "service-template-filename" in body:
    service_template_filename = body["service-template-filename"]
  else:
    service_template_filename = "service-template.yaml"

  service_template_path = service_template_utils.get(service_template_path,
                                                     service_template_filename)
  
  core = Core(model_storage, resource_storage, plugin_manager)
  core.validate_service_template(service_template_path)

  logger.info('Service template {} validated'.format( service_template_path))
  return "", 200

# delete template
@app.route(route_base + "templates/<template_id>", methods = ['DELETE'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_resource_storage
@aria.pass_plugin_manager
@aria.pass_logger
def delete_template( template_id, model_storage, resource_storage, plugin_manager, logger ):

  core = Core(model_storage, resource_storage, plugin_manager)
  core.delete_service_template(template_id)

  logger.info('Service template {} deleted'.format( template_id))
  return "", 200

# list templates
@app.route(route_base + "templates", methods = ['GET'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_logger
def list_templates( model_storage, logger):
  list = model_storage.service_template.list()
  templates = []
  for item in list:
    templates.append({ "name" : item.name, "id" : item.id })
  return jsonify(templates)

# list nodes
@app.route(route_base + "templates/<template_id>/nodes", methods = ['GET'])
@auto.doc()
@aria.pass_model_storage
def list_nodes(template_id, model_storage):
#  service_template = model_storage.service_template.get(template_id)
#  filters = dict(service_template=service_template)
#  nodes = model_storage.node_template.list(filters)
#  return jsonify(nodes), 200
  return "not implemented",501
  
# show node details
@app.route(route_base + "templates/nodes/<node_id>", methods = ['GET'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_logger
def get_node(node_id, model_storage, logger):
  node_template = model_storage.node_template.get(node_id)
  retmap = {}
  retmap['id'] = node_id
  retmap['name'] = node_template.name
  if node_template.properties:
    plist = []
    for prop in node_template.properties:
      plist.append({prop:node_template.properties[prop].type_name})
    retmap['properties'] = plist
  else:
    return "{} not found".format(node_id), 404
  return jsonify(retmap), 200

###
### SERVICES
###

# list services
@app.route(route_base + "services", methods = ['GET'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_logger
def list_services(model_storage, logger):
  services_list = model_storage.service.list()
  outmap = {}
  for service in services_list:
    outmap[service.name] = {"id":service.id, "description":service.description,
                    "name":service.name, "service_template": service.service_template.name,
                    "created":service.created_at, "updated":service.updated_at}
  return jsonify(outmap), 200

# show service
@app.route(route_base + "services/<service_id>", methods = ['GET'])
def show_service(service_id):
  return "not implemented",501

# get service outputs
@app.route(route_base + "services/<service_id>/outputs", methods = ['GET'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_logger
def get_service_outputs(service_id, model_storage, logger):
  service = model_storage.service.get(service_id)
  outlist = []
  for output_name, output in service.outputs.iteritems():
    outlist.append({"name":output_name, "description":output.description, 
                    "value":output.value})
  return jsonify(outlist)

# get service inputs
@app.route(route_base + "services/<service_id>/inputs", methods = ['GET'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_logger
def get_service_inputs(service_id, model_storage, logger):
  service = model_storage.service.get(service_id)
  outlist = []
  for input_name, input in service.inputs.iteritems():
    outlist.append({"name":input_name, "description":input.description, 
                    "value":input.value})
  return jsonify(outlist)

# create service
@app.route(route_base + "services", methods = ['POST'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_resource_storage
@aria.pass_plugin_manager
@aria.pass_logger
def create_service(model_storage, resource_storage,
                   plugin_manager, logger):
  body = request.json
  inputs = {}
  if 'inputs' in body:
    inputs = body['inputs']
  if 'service_template_id' not in body:
    return "body missing service_template_id", 400
  if 'service_name' not in body:
    return "body missing service_name", 400
  core = Core(model_storage, resource_storage, plugin_manager)
  service = core.create_service(body["service_template_id"], inputs, body['service_name'])

  logger.info("service {} created".format(service.name))
  return "service {} created".format(service.name), 200
  

# delete service
@app.route(route_base + "services/<service_id>", methods = ['DELETE'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_model_storage
@aria.pass_resource_storage
@aria.pass_plugin_manager
@aria.pass_logger
def delete_service(service_id, model_storage, resource_storage, plugin_manager, logger):
  service = model_storage.service.get(service_id)
  core = Core(model_storage, resource_storage, plugin_manager)
  core.delete_service(service_id, force = True)
  return "service {}  deleted".format(service.id), 200
  

###
### WORKFLOWS
###

# list workflows
@app.route(route_base + "services/<service_id>/workflows", methods = ['GET'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_logger
def list_workflows(service_id, model_storage, logger):
  service = model_storage.service.get(service_id)
  workflows = service.workflows.itervalues()
  outlist = []
  for workflow in workflows:
    outlist.append(workflow.name)
  return jsonify(outlist), 200
  

# show workflow
@app.route(route_base + "services/<service_id>/workflow/<workflow_name>", methods = ['GET'])
def show_workflows(service_name, workflow_name):
  return "not implemented",501

###
### EXECUTIONS
###

# list all executions
@app.route(route_base + "executions", methods = ['GET'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_logger
def list_executions(model_storage,logger):
  elist = model_storage.execution.list() 
  outlist = []
  for execution in elist:
    outlist.append({"execution_id":execution.id,
                    "workflow_name":execution.workflow_name,
                    "service_template_name":execution.service_template_name,
                    "service_name":execution.service_name,
                    "status":execution.status})
  return jsonify(outlist), 200
  
# list executions for service
@app.route(route_base + "services/<service_id>/executions", methods = ['GET'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_logger
def list_service_executions(service_id, model_storage, logger):
  service = model_storage.service.get(service_id)
  elist = model_storage.execution.list(filters=dict(service=service))
  outlist = []
  for execution in elist:
    outlist.append({"execution_id":execution.id,
                    "workflow_name":execution.workflow_name,
                    "service_template_name":execution.service_template_name,
                    "service_name":execution.service_name,
                    "status":execution.status})
  return jsonify(outlist), 200

# show execution
@app.route(route_base + "executions/<execution_id>", methods = ['GET'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_logger
def show_execution(execution_id, model_storage, logger):

  try:
    execution = model_storage.execution.get(execution_id)
  except:
    return "Execution {} not found".format(execution_id), 404

  return jsonify({"execution_id":execution_id, "service_name":execution.service_name,
          "service_template_name":execution.service_template_name,
          "workflow_name":execution.workflow_name,
          "status":execution.status}), 200

# start execution
@app.route(route_base + "executions/<service_id>/<workflow_name>", methods = ['POST'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_resource_storage
@aria.pass_plugin_manager
@aria.pass_logger
def start_execution(service_id, workflow_name, model_storage, resource_storage, plugin_manager, logger):
  body = request.json
  service = model_storage.service.get(service_id)
  executor = DryExecutor() if 'executor' in body and body['executor'] == 'dry' else None

  inputs = body['inputs'] if 'inputs' in body else None
  task_max_attempts = ( body['task_max_attempts']
                        if 'task_max_attempts' in body else 30 )
  task_retry_interval = ( body['task_retry_interval'] 
                          if 'task_retry_interval' in body else 30 )

  runner = WorkflowRunner(model_storage, resource_storage, plugin_manager,
                          service_id = service_id,
                          workflow_name = workflow_name,
                          inputs = inputs,
                          executor = executor,
                          task_max_attempts =  task_max_attempts,
                          task_retry_interval = task_retry_interval)

  tname = '{}_{}'.format(service.name,workflow_name)
  thread = threading.ExceptionThread(target = runner.execute,
                                     name = tname)
  thread.start()
  return jsonify({"id":runner.execution_id}), 202

## resume execution
@app.route(route_base + "executions/<execution_id>", methods = ['POST'])
@auto.doc()
@aria.pass_model_storage
@aria.pass_resource_storage
@aria.pass_plugin_manager
@aria.pass_logger
def resume_execution(execution_id, model_storage, resource_storage, plugin_manager, logger):
  body = request.json
  execution = model_storage.execution.get(execution_id)
  if execution.status != execution.status.CANCELLED:
    return "cancelled execution cannot be resumed", 400
  executor = DryExecutor() if 'executor' in body and body['executor'] == 'dry' else None
  
  runner = WorkflowRunner(model_storage, resource_storage, plugin_manager,
                          service_id = service_id,
                          workflow_name = workflow_name,
                          executor = executor,
                          execution_id = execution_id,
                          task_max_attempts =  task_max_attempts,
                          task_retry_interval = task_retry_interval)

  tname = '{}_{}'.format(service.name,workflow_name)
  thread = threading.ExceptionThread(target = runner.execute,
                                     name = tname,
                                     daemon = True )
  execution_thread.start()
  return jsonify({"id":runner.execution_id}), 202

## cancel execution
@app.route(route_base + "executions/<execution_id>", methods = ['DELETE'])
def cancel_execution(execution_id):
  return "not implemented",501


if __name__ == "__main__":
  app.run(threaded = True)

