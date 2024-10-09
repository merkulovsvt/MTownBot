from aiogram.filters.callback_data import CallbackData


class LeadStartUpload(CallbackData, prefix="lead_start_upload"):
    lead_id: int


class RetrySearch(CallbackData, prefix="retry_search"):
    lead_id: int
