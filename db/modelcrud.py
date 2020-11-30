from sqlalchemy.orm import Session


class ModelCRUD:
    def __init__(self, model, db: Session):
        if not callable(model):
            raise RuntimeError(f'The {model} is not a callable object')
        self.model = model
        self.db = db

    def get_all(self, offset: int = 0, limit: int = 100):
        self.db.query(self.model).offset(offset).limit(limit).all()

    def add_new(self, **data):
        db_model = self.model(**data)
        self.db.add(db_model)
        self.db.commit()
        self.db.refresh(db_model)
        return db_model

    def filter(self, *conditions):
        resp = self.db.query(self.model).filter(*conditions)
        return resp

    def get_first(self, *conditions):
        result = self.filter(*conditions).first()
        return result

    def update(self, values: dict, *conditions):
        result = self.filter(*conditions).update(values)
        self.db.commit()
        return result

    def delete(self, *conditions):
        result = self.filter(*conditions).delete()
        self.db.commit()
        return result
