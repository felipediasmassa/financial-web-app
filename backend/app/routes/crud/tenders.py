"""
Module to handle requests to entity 'Tenders'
"""

from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session

from dependencies import get_db
from utils import upsert_object, add_and_commit, convert_to_dict
from utils.check_db_status import check_table_status_decorator
from utils.get_user_data import process_roles


class TendersRouter(APIRouter):
    def __init__(self, data_model):
        super().__init__()
        Tender = data_model.Tender

        @self.get("/read-tenders")
        @check_table_status_decorator(Tender, "Tender")
        async def read_tenders(db_session: Session = Depends(get_db)) -> list[dict]:

            return db_session.query(Tender).all()

        @self.get("/read-tender-by-id/{tender_id}")
        @check_table_status_decorator(Tender, "Tender")
        async def read_tender_by_id(
            tender_id: int, db_session: Session = Depends(get_db)
        ) -> dict:

            tender = db_session.query(Tender).filter(Tender.id == tender_id).first()

            if tender:
                return tender

            raise HTTPException(
                status_code=404,
                detail=f"Not Found: tender with id {tender_id} not found in database",
            )

        @self.get("/read-tenders-by-roles/{grid_mode}/{roles}")
        @check_table_status_decorator(Tender, "Tender")
        async def read_tenders_by_roles(
            grid_mode: str, roles: str, db_session: Session = Depends(get_db)
        ) -> dict:

            # Processing role string and returning tenders with read and write permissions
            roles = process_roles(roles)

            # Raising error if grid_mode value passed is not acceptable:
            if not grid_mode == "read" and not grid_mode == "write":
                raise HTTPException(
                    status_code=400,
                    detail=f"Grid mode must be 'read' or 'write'. Value '{grid_mode}' was passed",
                )

            # Defining allowed tenders as those for which user has "read" or "write" permission
            # (based on grid_mode):
            allowed_tenders = roles[grid_mode]

            # Filtering allowed tenders:
            tenders = (
                db_session.query(Tender)
                .filter(Tender.tender.in_(allowed_tenders))
                .all()
            )

            return tenders

        @self.post("/create-tender")
        @check_table_status_decorator(Tender, "Tender")
        async def create_tender(
            tender: dict, db_session: Session = Depends(get_db)
        ) -> dict:

            # Creating object to store new tender:
            new_tender = Tender()

            # Returning error if there is column "id" in post request:
            if "tender_id" in tender:
                raise HTTPException(
                    status_code=400,
                    detail="Bad Request: column id should not be in post request body",
                )

            # Passing properties to new_tender object:
            new_tender = upsert_object(tender, new_tender)

            # Adding and commiting to database:
            add_and_commit(new_tender, db_session)

            # Crafting dictionary to return:
            tender_dict = convert_to_dict(new_tender)

            return {
                "message": f"Tender added with id {new_tender.id}",
                **tender_dict,
            }

        @self.put("/update-tender/{tender_id}")
        @check_table_status_decorator(Tender, "Tender")
        async def update_tender(
            tender_id: int, tender: dict, db_session: Session = Depends(get_db)
        ) -> dict:

            response = update_one_tender(Tender, tender, tender_id, db_session)

            return response

        @self.delete("/delete-tenders")
        @check_table_status_decorator(Tender, "Tender")
        async def delete_tenders(
            tenders_ids: list[int], db_session: Session = Depends(get_db)
        ) -> dict:

            response = []

            for tender_id in tenders_ids:

                delete_tender = db_session.get(Tender, tender_id)
                if not delete_tender:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Not Found: tender with id {tender_id} not found in database",
                    )

                db_session.delete(delete_tender)
                db_session.commit()

                response.append({"message": f"Tender deleted with id {tender_id}"})

            return response


def update_one_tender(Tender, tender, tender_id, db_session):

    """Function to update one tender in database"""

    # Renaming key "tender_id" to "id" (to match with table column name):
    tender["id"] = tender.pop("tender_id")

    # Finding tender with tender_id:
    query = db_session.query(Tender).filter(Tender.id == tender_id)
    update_tender = query.first()

    # Returning error if no record was found with the given id:
    if not update_tender:
        raise HTTPException(
            status_code=404,
            detail=f"Not Found: tender with id {tender_id} not found in database",
        )

    # Passing properties to update_tender object:
    update_tender = upsert_object(tender, update_tender)

    # Adding and commiting to database:
    add_and_commit(update_tender, db_session)

    # Crafting dictionary to return:
    tender_dict = convert_to_dict(update_tender)

    return {
        "message": f"Tender updated with id {update_tender.id}",
        **tender_dict,
    }
