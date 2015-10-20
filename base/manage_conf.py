from yatu import settings, bootstrap
import inject

bootstrap(settings)

uow = inject.instance('UnitOfWorkManager')
db_tx = uow.start().__enter__()

yatu_user = db_tx.users.get_by_token('NyaWDJekdjWI38KejJWlkd93jsdtu')



