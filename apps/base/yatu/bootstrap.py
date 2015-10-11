import inject
from yatu.orm import SqlAlchemy
from yatu.shortifiers import UUIDShortifier


def bootstrap(config):
    dal = SqlAlchemy(config['postgres_conn_string'])
    dal.configure_mappings()

    # configure bindings
    unit_of_work_manager = dal.unit_of_work_manager()
    inject.configure_once(
        lambda binder: binder.bind(
            'UnitOfWorkManager', unit_of_work_manager
        ).bind(
            'Shortifier', UUIDShortifier()
        )
    )

