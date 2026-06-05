{{ config(materialized='ephemeral') }}

select
    messageid,
    tenantid,
    channeltype,
    direction,
    address,
    deliverystatus,
    sentorreceivedat,
    "_fetched_at",
    "_source"
from {{ source('raw', 'edna') }}
limit 10
