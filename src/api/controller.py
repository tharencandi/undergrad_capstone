from flask import Blueprint, jsonify
from celery.result import AsyncResult


api = Blueprint("api", import_name=__name__)

"""
Get a list of all whole slide images and their associated files
"""
@api.get("/wholeslides")
def get_all_wholeslides():
    # check query string for specific wholeslide uuids
    # return a dict with 
    response = """
    {
        wholeslides: [
            {
                uuid: string,
                size: int,
                description: string
                mask: {
                    generated: boolean
                    mask_id: string
                }
                associated_files: [
                    {
                        fname: string,
                        ftype: string,
                        fsize: string
                        description: string
                    }
                ]
            }
        ]
    }
    """

@api.get("/wholeslides/<uuid>/data")
def download_data():
    # download a wholeslide image
    response = """
    {
        uuid: string,
        size: int,
        description: string
    }

    Attachment: file data
    """
    pass


@api.post("/wholeslides")
def upload_wholeslide():
    # upload one wholeslide image
    request = """
    {
        uuid: string,
        size: int,
        description: string
    }

    Attachment: file data
    """
    pass

@api.post("/wholeslides/mask")
def segment_wholeslides():
    # ask the server to segment a list of wholeslide images
    request = """
    {
        wholeslides: [
            uuid1,
            uuid2,
            uuid3,
        ]
    }
    """

    response = """
    {
        jobs: [
            job_id1,
            job_id2,
            job_id3
        ]
    }
    """

@api.post("/job/status")
def get_jobs_status():
    # ask server for status update on jobs. Once a job has been completed, can get the mask using endpoint below
    request = """
    {
        jobs: [
            job_id,
            job_id2
        ]
    }
    """

    response = """
    {
        jobs [
            {
                job_id: string,
                staus: [PENDING, STARTED, FAILURE, SUCCESS]
            },
            {
                job_id: string,
                status: [PENDING, STARTED, FAILURE, SUCCESS]
            }
        ]
    }
    """
@api.get("/wholeslides/<uuid>/mask")
def get_wholeslide_mask():
    response="""
    {
        uuid
    }

    Attachment
    """

@api.post("/wholeslides/files")
def convert_wholeslides():
    request = """
    {
        conversions: [
            {
                uuid: string
                output_type: [PNG, JPEG, TITF]
                fname: string
            },
            {
                uuid: string
                output_type: [PNG, JPEG, TITF]
                fname: string
            }
        ]
    }
    """
    response = """
     {
        jobs: [
            job_id1,
            job_id2
        ]
     }
    """
@api.get("wholeslides/<uuid>/files/<fname>/data")
def get_wholeslide_file(uuid, fname):
    response = """
    {
        fname: string,
        ftype: string
        description: string,
    }

    Attachment: file data
    """
@api.get("wholeslides/<uuid>/files")
def list_wholeslide_files(uuid):
    response = """
    {
        files [
            {
                fname: string,
                ftype: string.
                description: string
            }
        ]
    }
    """
# list all whole slide /
# upload wholeslide /
# download wholeslide /
# segment wholeslide /
# convert wholeslide /
#download converted files /
# list converted files for a whileslide /
# list all converted files
# get file metadata