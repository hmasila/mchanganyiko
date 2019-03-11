import MySQLdb
from flask import Flask, request, jsonify, send_from_directory
import json

from flask import make_response
import os




# Flask App
app = Flask(__name__)


@app.route("/")
def main():
    db = MySQLdb.connect(
            host="0.0.0.0",
            user="root",
            passwd="",
            db="db_name",
        )
    cur = db.cursor()
    cur.execute(
        "SELECT DISTINCT(sensor_name) FROM nectar_sensor_data.master_sensor_data WHERE timestamp >= DATE_SUB(NOW(),INTERVAL 15 MINUTE);"
    )
    active_sensor_list = []
    rv = cur.fetchall()
    for sensor in rv:
        active_sensor_list.append(sensor)

    db.close()
    return "Active sensors within the last 15 minutes {}".format(
        list(active_sensor_list[i][0] for i in range(0, len(active_sensor_list)))
    )

#Route lists sensors updated within the last 30 seconds
@app.route("/recent")
def recent():
    db = MySQLdb.connect(
        host="nectardb.mysql.database.azure.com",
        user="adi@nectardb",
        passwd="master1234",
        db="nectar_sensor_data",
    )
    cur = db.cursor()
    cur.execute(
        "SELECT DISTINCT(sensor_name) FROM nectar_sensor_data.master_sensor_data WHERE timestamp >= DATE_SUB(NOW(),INTERVAL 30 SECOND);"
    )
    active_sensor_list = []
    rv = cur.fetchall()
    for sensor in rv:
        active_sensor_list.append(sensor)

    db.close()
    return "Active sensors within the last 30 seconds {}".format(
        list(active_sensor_list[i][0] for i in range(0, len(active_sensor_list)))
    )

#Route lists sensors updated within the last 1 hour
@app.route("/lasthour")
def hour():
    db = MySQLdb.connect(
            host="0.0.0.0",
            user="root",
            passwd="",
            db="db_name",
        )
    cur = db.cursor()
    cur.execute(
        "SELECT DISTINCT(sensor_name) FROM nectar_sensor_data.master_sensor_data WHERE timestamp >= DATE_SUB(NOW(),INTERVAL 1 HOUR);"
    )
    active_sensor_list = []
    rv = cur.fetchall()
    for sensor in rv:
        active_sensor_list.append(sensor)

    db.close()
    return "Active sensors within the last 1 hour {}".format(
        list(active_sensor_list[i][0] for i in range(0, len(active_sensor_list)))
    )




@app.route("/post", methods=["POST"])
# @auth.login_required
def post():
    if (
        request.method == "POST"
    ):  # this block is only entered when the form is submitted
        db = MySQLdb.connect(
            host="0.0.0.0",
            user="db_user",
            passwd="db_pass",
            db="db_name",
        )
        cur = db.cursor()
        hw_version = request.form.get("hw_version")
        packet_version = request.form.get("packet_version")
        sequence_number = request.form.get("sequence_number")
        reserved = request.form.get("reserved")
        timestamp = request.form.get("timestamp")
        sensor_name = request.form.get("sensor_name")
        channel_1_current = request.form.get("channel_1_current")
        channel_1_counts = request.form.get("channel_1_counts")
        channel_1_gain = request.form.get("channel_1_gain")
        channel_2_current = request.form.get("channel_2_current")
        channel_2_counts = request.form.get("channel_2_counts")
        channel_2_gain = request.form.get("channel_2_gain")
        glucose_flags = request.form.get("glucose_flags")
        glucose_data = request.form.get("glucose_data")
        misc_data = request.form.get("misc_data")
        smbg_reading = request.form.get("smbg_reading")


        sql_stmnt = (
            "INSERT INTO nectar_sensor_data.master_sensor_data (hw_version, packet_version, sequence_number, reserved, timestamp, sensor_name, channel_1_current, channel_1_counts, channel_1_gain, channel_2_current, channel_2_counts, channel_2_gain, glucose_flags, glucose_data, misc_data,smbg_reading) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;"
        )

        sql_data = (
            hw_version,
            packet_version,
            sequence_number,
            reserved,
            timestamp,
            sensor_name,
            channel_1_current,
            channel_1_counts,
            channel_1_gain,
            channel_2_current,
            channel_2_counts,
            channel_2_gain,
            glucose_flags,
            glucose_data,
            misc_data,
            smbg_reading
        )

        cur.execute(sql_stmnt, sql_data)

        db.commit()
        db.close()

    return """
    Success!
    HW Version:{} Packet Version:{} Sequence Number:{} Reserved:{} Timestamp:{} Sensor Name:{} channel_1_current:{} channel_1_counts:{} channel_1_gain:{} channel_2_current:{} channel_1_counts:{} channel_2_gain: {}Glucose Flags:{} Glucose Data:{} Misc Data: {} SMBG Reading : {}



              """.format(
        hw_version,
        packet_version,
        sequence_number,
        reserved,
        timestamp,
        sensor_name,
        channel_1_current,
        channel_1_counts,
        channel_1_gain,
        channel_2_current,
        channel_2_counts,
        channel_2_gain,
        glucose_flags,
        glucose_data,
        misc_data,
        smbg_reading
    )

@app.route('/api/v1/swagger')
def documentation():
    datastore = {}
    with open('swagger.json', 'r') as f:
        datastore = json.load(f)
    return jsonify(datastore)

@app.route('/api/documentation')
def render_documentation():
    data = open('api.html').read()
    return data

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5007))
    app.run(host="0.0.0.0", port=port, debug=True)
