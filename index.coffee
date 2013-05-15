# Description:
#   None
#
# Dependencies:
#   None
#
# Configuration:
#   None
#
# Author:
#   maxgoedjen


class PythonScript
    
  pyScriptPath = __dirname + '/python_dispatch.py'
  python_script = require('child_process').spawn('python', [pyScriptPath])
  python_script.stdout.on 'data', (data) =>
    receive_from_python(data.toString())

  module.exports = (robot) ->
    @robot = robot
    robot.respond /(.*)/i, (msg) ->
      newRegex = new RegExp("^[@]?#{robot.name}[:,]? ?(.*)", 'i')
      match = newRegex.exec msg.message.text
      send_to_python(match[1], msg.message.room, 'respond')
    robot.hear /(.*)/i, (msg) ->
      send_to_python(msg.message.text, msg.message.room, 'hear')

  send_to_python = (message, room, method) ->
    dict = 
      type : method,
      message : message,
      room : room
    python_script.stdin.write(JSON.stringify(dict) + '\n')

  receive_from_python = (json) ->
    data = JSON.parse(json)
    @robot.messageRoom data.room, data.message
