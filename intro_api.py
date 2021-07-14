from flask import Flask, request
from multiprocessing import Process

from waitress import serve
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=["GET"])
def hello_world():
    return "Hello, World!"


@app.route("/task/<uuid:job_id>", methods=["POST"])
def task(job_id):
    # check the valid input
    body_job_id = request.json.get("job_id")
    body_operator = request.json.get("operator")

    if is_valid_request(body_job_id, body_operator) == False:
        return (
            "Bad request, invalid job_id: %s or operator: %s"
            % (body_job_id, body_operator),
            401,
        )

    task_cb = Process(target=run_task, args=(body_job_id, body_operator))
    task_cb.start()
    return "Job_id %s received!" % job_id, 202


def run_task(job_id, job_operator):
    # ready to process the job
    # it is important to keep the gap between has_waiting_job_bucket()
    # set WAITING_STATUS as small as possible to avoid extreme cases
    update_job_status(job_id, consts.WAITING_STATUS)
    log_process = "Processing job_id: %s, job_operator: %s \n" % (job_id, job_operator)
    logging.info(log_process)

    # start to process the bidding
    while get_num_jobs(consts.RUNNING_STATUS) > consts.MAX_NUM_CONCURRENT_RUNNING_JOBS:
        # it is possible the later received jobs will jump out of this while
        # loop first than the earlier received jobs
        # Queue can be a solution to this, but then we need a background worker to
        # pick up the jobs in queue
        time.sleep(consts.SLEEPING_SECONDS)

    # there is extreme case that two jobs are freed out from while loop
    # at the same instance

    # there is worker to run this job
    # lock this worker for running this job
    update_job_status(job_id, consts.RUNNING_STATUS)
    try:
        # simulate a time expensive task
        time.sleep(500)
        # finish job running, unlock the worker
        update_job_status(job_id, consts.COMPLETED_STATUS)
    except:
        update_job_status(job_id, consts.FAILED_STATUS)
        log_error = "Error: bidding job failed for job_id %s\n" % job_id
        raise Exception(log_error)
        abort(403)


if __name__ == "__main__":
    # debug mode
    # app.run(host='0.0.0.0', debug=True, port=6060)
    # production mode
    serve(app, port=6060)
