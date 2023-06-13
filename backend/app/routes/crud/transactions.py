"""Module to handle requests to entity 'Transactions'"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import utils.dependencies as dp
import utils.crud as cr


class TransactionsRouter(APIRouter):
    def __init__(self, data_model):
        super().__init__()
        Transaction = data_model.Transaction

        @self.get("/read-transactions")
        async def read_transactions(db_session: Session = Depends(dp.get_db)) -> list:
            return db_session.query(Transaction).all()

        @self.get("/read-transaction-by-id/{transaction_id}")
        async def read_transaction_by_id(
            transaction_id: int, db_session: Session = Depends(dp.get_db)
        ) -> dict:
            transaction = (
                db_session.query(Transaction)
                .filter(Transaction.id == transaction_id)
                .first()
            )

            if transaction:
                return cr.convert_to_dict(transaction)

            raise HTTPException(
                status_code=404,
                detail=f"Not Found: transaction with id {transaction_id} not found in database",
            )

        @self.post("/create-transaction")
        async def create_transaction(
            transaction: dict, db_session: Session = Depends(dp.get_db)
        ) -> dict:
            # Creating object to store new transaction:
            new_transaction = Transaction()

            # Returning error if there is column "id" in post request:
            if "transaction_id" in transaction:
                raise HTTPException(
                    status_code=400,
                    detail="Bad Request: column id should not be in post request body",
                )

            # Passing properties to new_transaction object:
            new_transaction = cr.upsert_object(transaction, new_transaction)

            # Adding and commiting to database:
            cr.add_and_commit(new_transaction, db_session)

            # Crafting dictionary to return:
            transaction_dict = cr.convert_to_dict(new_transaction)

            return {
                "message": f"Transaction added with id {new_transaction.id}",
                **transaction_dict,
            }

        @self.put("/update-transaction/{transaction_id}")
        async def update_transaction(
            transaction_id: int,
            transaction: dict,
            db_session: Session = Depends(dp.get_db),
        ) -> dict:
            response = update_one_transaction(
                Transaction, transaction, transaction_id, db_session
            )

            return response

        @self.delete("/delete-transactions")
        async def delete_transactions(
            transactions_ids: list[int], db_session: Session = Depends(dp.get_db)
        ) -> list[dict]:
            response = []

            for transaction_id in transactions_ids:
                delete_transaction = db_session.get(Transaction, transaction_id)
                if not delete_transaction:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Not Found: transaction with id {transaction_id} not found in database",
                    )

                db_session.delete(delete_transaction)
                db_session.commit()

                response.append(
                    {"message": f"Transaction deleted with id {transaction_id}"}
                )

            return response


def update_one_transaction(Transaction, transaction, transaction_id, db_session):
    """Function to update one transaction in database"""

    # Returning error if transaction_id or id is passed in request body (instead of query
    # parameter):
    if transaction.get("id") or transaction.get("transaction_id"):
        raise HTTPException(
            status_code=400,
            detail="Bad Request: column id / transaction_id should not be in post request body",
        )

    # Renaming key "transaction_id" to "id" (to match with table column name):
    transaction["id"] = transaction_id

    # Finding transaction with transaction_id:
    query = db_session.query(Transaction).filter(Transaction.id == transaction_id)
    update_transaction = query.first()

    # Returning error if no record was found with the given id:
    if not update_transaction:
        raise HTTPException(
            status_code=404,
            detail=f"Not Found: transaction with id {transaction_id} not found in database",
        )

    # Passing properties to update_transaction object:
    update_transaction = cr.upsert_object(transaction, update_transaction)

    # Adding and commiting to database:
    cr.add_and_commit(update_transaction, db_session)

    # Crafting dictionary to return:
    transaction_dict = cr.convert_to_dict(update_transaction)

    return {
        "message": f"Transaction updated with id {update_transaction.id}",
        **transaction_dict,
    }
