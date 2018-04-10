from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import numpy as np
import tensorflow as tf
import os
import json
import tempfile
import urllib

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)

    return graph


@app.route('/pred', methods=['POST'])
@cross_origin()
def index():
    predList = []
    reqContent = request.get_json(silent=True)
    print(reqContent)
    print(reqContent['snp_log_return_1'])

    with tf.Session(graph=graph) as sess:
        try:
            inputVal = np.array([[reqContent['snp_log_return_1'],
                                  reqContent['snp_log_return_2'],
                                  reqContent['snp_log_return_3'],
                                  reqContent['nyse_log_return_1'],
                                  reqContent['nyse_log_return_2'],
                                  reqContent['nyse_log_return_3'],
                                  reqContent['djia_log_return_1'],
                                  reqContent['djia_log_return_2'],
                                  reqContent['djia_log_return_3'],
                                  reqContent['nikkei_log_return_0'],
                                  reqContent['nikkei_log_return_1'],
                                  reqContent['nikkei_log_return_2'],
                                  reqContent['hangseng_log_return_0'],
                                  reqContent['hangseng_log_return_1'],
                                  reqContent['hangseng_log_return_2'],
                                  reqContent['dax_log_return_0'],
                                  reqContent['dax_log_return_1'],
                                  reqContent['dax_log_return_2'],
                                  reqContent['aord_log_return_0'],
                                  reqContent['aord_log_return_1'],
                                  reqContent['aord_log_return_2']]])
            expectClass = np.array([[reqContent['snp_log_return_positive'],
                                     reqContent['snp_log_return_negative']]])
            results, pred = sess.run([output_operation.outputs[0], pred_operation.outputs[0]], {
                input_operation.outputs[0]: inputVal,
                class_operation.outputs[0]: expectClass
            })

            top_k = results.argsort()
            labels = []
            labels.append("Positive")
            labels.append("Negative")
            for idx, i in enumerate(top_k):
                ix = i[-1]
                res = {}
                res["label"] = labels[ix]
                res["score"] = str(results[idx][ix])
                predList.append(res)
            # predList.append(arr)

            print(predList)
            # os.remove(file_name)
        except Exception, e:
            print(str(e))
            response = jsonify("exception raised")
            response.status_code = 500
            return response
          # print(json.dumps(res, ensure_ascii=False))
    return jsonify(predList)


if __name__ == '__main__':
    file_name = ""
    model_file = "/model.pb"
    # model_file = "/model-cpu.pb"
    input_layer = "input"
    output_layer = "model"
    class_layer = "import/classes"
    pred_layer = "import/pred"

    graph = load_graph(model_file)

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)
    class_operation = graph.get_operation_by_name(class_layer)
    pred_operation = graph.get_operation_by_name(pred_layer)

    app.run(host='0.0.0.0', port=6006, debug=True)
