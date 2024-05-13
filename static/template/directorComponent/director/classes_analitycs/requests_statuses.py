from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, cast, Date, func, literal, union_all
import datetime

from models_db.models_request import Requests, Status

class requeestsStatusesService:
    def __init__(self, engine_a):
        self.engine_a = engine_a

    async def get_status_names(self):
        async with AsyncSession(self.engine_a) as session:
            query_status = (
                select(
                    Status.name,
                )
                .select_from(Status)
            )
            result_status = await session.execute(query_status)
            rows_status = result_status.fetchall()

        return [row[0] for row in rows_status]

    async def get_count_status_from_dates(self, status_names, start_date, end_date):
        async with AsyncSession(self.engine_a) as session:
            queries = []
            start_date, end_date = self.transformation_dates(start_date, end_date)
            for status in status_names:
                query = (
                    select(
                        cast(Requests.submissiondate, Date).label('submission_date'),
                        func.count(Requests.id).label('data_count'),
                        literal(status).label('status_name')
                    )
                    .join(Status, Requests.statusid == Status.id)
                    .where(
                        and_(
                            cast(Requests.submissiondate, Date) >= start_date,
                            cast(Requests.submissiondate, Date) <= end_date,
                            Status.name == status
                        )
                    )
                    .group_by('submission_date', 'status_name')
                )
                queries.append(query)

            combined_query = union_all(*queries)

            result = await session.execute(combined_query)
            rows = result.all()

            data_dict = {}
            total_dict = {}
            for submission_date in self.daterange(start_date, end_date):
                formatted_date = submission_date.strftime('%Y-%m-%d')
                data_dict[formatted_date] = {status: 0 for status in status_names}
                total_dict[formatted_date] = 0

            for row in rows:
                submission_date = row.submission_date.strftime('%Y-%m-%d')
                data_dict[submission_date][row.status_name] = row.data_count
                total_dict[submission_date] += row.data_count

            transformed_dict = {}
            for submission_date in data_dict.keys():
                transformed_dict[submission_date] = {
                    'всего': total_dict[submission_date],
                    **data_dict[submission_date]
                }

            return transformed_dict


    @staticmethod
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + datetime.timedelta(n)

    @staticmethod
    def transformation_dates(start_date, end_date):
        start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        return start_date_obj, end_date_obj
