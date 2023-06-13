from fastapi import HTTPException
from sqlalchemy.orm.attributes import instance_dict


def upsert_object(request_body, db_object):
    """Function to iterate in update database object based only on keys passed in request"""

    for key, value in request_body.items():
        if key in dir(db_object):
            setattr(db_object, key, value)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Bad Request: column {key} not found in table",
            )

    return db_object


def add_and_commit(new_record, db_session):
    """Function to add and commit record to database"""

    # Adding new record to database:
    try:
        db_session.add(new_record)
        db_session.commit()
    except Exception as err:
        raise HTTPException(
            status_code=401,
            detail=str(err),
        ) from err


def convert_to_dict(record):
    """Function to convert database object to dictionary for output response"""

    # Returning new id so that, when using instance_dict, a non-empty dictionary is returned:
    _ = record.id

    # Converting class object to dictionary to output in response:
    record_dict = instance_dict(record)
    record_dict.pop("_sa_instance_state", None)

    return record_dict
