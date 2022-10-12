import cx_Oracle
import pandas as pd
import timeit

from pandas.core.frame import DataFrame

login_info = ['', '']

def trial_1(login_info):
    dsn_tns = cx_Oracle.makedsn('ora-tns-qcc1.in.qservco.com', 1521, service_name = 'qcc1' )
    connection = cx_Oracle.connect(
        user = login_info[0],
        password = login_info[1],
        dsn = dsn_tns)
    print('='*60)
    print('\t - Connection established.')
    query = '''
select distinct
    s.sub_id, s.sub_nm, to_char(invoice.trans_dttm, 'YYYY-MM-DD') as invoice_dt,
    invoice.amt as invoice_sum_amt,
    to_char(min(payment.trans_dttm), 'YYYY-MM-DD') as min_payment_dt,
    to_char(max(payment.trans_dttm), 'YYYY-MM-DD') as max_payment_dt, 
    sum(payment.amt) as payment_sum_amt, count(payment.amt) as count_of_payment,
    round(sum(payment.amt)/count(payment.amt), 2) as avg_payment,
    listagg(invoice.trans_nm, '; ') as transactions
from
    (
        select
            max(trans_dttm) as trans_dttm, sum(amt) as amt,
            trans_nm, sub_id
        from wasabi.v_trans t,
        (
            select
                trans_typ, trans_nm
            from wasabi.v_trans_typ
            where lower(trans_nm) like '%equip%nrc%'
        ) nm
        where t.trans_cls = 'R'
            and t.amt > 0
            and (t.trans_stat = 'I' or t.trans_stat = 'C')
            and t.trans_dttm >= add_months(trunc(sysdate), -6)
            and t.trans_typ in nm.trans_typ
        group by trans_nm, sub_id, trans_cls
    ) invoice,
    (
        select
            trans_dttm, amt, sub_id
        from wasabi.v_trans
        where trans_cls = 'P'
            and (trans_stat = 'I' or trans_stat = 'C')
    ) payment, wasabi.v_sub s
where payment.trans_dttm >= invoice.trans_dttm
and invoice.sub_id = s.sub_id
and payment.sub_id = s.sub_id
group by s.sub_id, s.sub_nm, invoice.amt, invoice.trans_dttm, invoice.trans_nm
    '''
    df = pd.read_sql(query, connection)
    print('\t - Read sql.')
    filename = 'Billed_Equipment_Paid_6mo.xlsx'
    sheetname = 'Subscribers & Equipment'
    writer = pd.ExcelWriter(filename, engine = 'xlsxwriter')
    df.to_excel(writer, sheet_name = sheetname, header = False, index = False)
    worksheet = writer.sheets[sheetname]
    (max_row, max_col) = df.shape
    headers = [{'header': header } for header in df.columns]
    worksheet.add_table(0, 0, max_row - 1, max_col - 1, {'columns': headers, 'style': 'Table Style Dark 5'})
    writer.save()
    print('\t - Finished.')

def trial_2(login_info): # Attempts to merge dataframes with two queries
    dsn_tns = cx_Oracle.makedsn('ora-tns-qcc1.in.qservco.com', 1521, service_name = 'qcc1' )
    connection = cx_Oracle.connect(
        user = login_info[0],
        password = login_info[1],
        dsn = dsn_tns)
    print('='*60)
    print('\t - Connection established.')
    query1 = '''
select distinct s.sub_id, s.sub_nm,
vtc.trans_dttm as latest_invoice_date,
vtp.trans_dttm as last_payment_date
from wasabi.v_srvc svc
join wasabi.v_sub s on s.sub_id = svc.sub_id
join wasabi.v_srvc_ct sct on sct.srvc_id = svc.srvc_id
join wasabi.v_ct_ct_num ccn on ccn.srvc_ct_id = sct.srvc_ct_id
join (
select * from wasabi.v_trans
where trans_cls = 'R'
and amt > 0
and trans_stat = 'I'
and trans_typ in (
select trans_typ from wasabi.v_trans_typ
where lower(trans_nm) like '%equip%'
)
) vtc on vtc.sub_id = s.sub_id
join (
select sub_id, max(trans_dttm) trans_dttm
from wasabi.v_trans
where trans_cls = 'P'
group by sub_id
) vtp on vtp.sub_id = s.sub_id
where svc.stat = 'A'
and (ccn.ct_num_typ = 21707 or ccn.ct_typ = 364)
and vtp.trans_dttm between trunc(sysdate)-30 and trunc(sysdate)
    '''
    query2 = '''
select 
sub_id, trans_dttm
from wasabi.v_trans
where trans_cls = 'P'
and sub_id = :sub_id
    '''
    df1 = pd.read_sql(query1, connection)
    print('\t - Read sql for df1.')
    df2 = DataFrame(columns = ['SUB_ID', 'TRANS_DTTM'])
    for row in df1['SUB_ID']:
        df2.append(pd.read_sql(query2, connection, params = {'sub_id': row}), ignore_index = True)
    # df2 = pd.read_sql(query2, connection, params = {'sub_id': df1['SUB_ID']}
    print('\t - Read sql for df2.')
    print(f'\t - DF1 Head:\n{df1.head}')
    print(f'\t - DF2 Head:\n{df2.head}')
    df = pd.merge(df1, df2)#, on = "sub_id")
    print('\t - Merged Dataframes.')
    print(f'\t - DF Info:\n{df.info}')
    print(f'\t - DF Head:\n{df.head}')
    filename = 'Billed_Equipment_Paid_6mo.xlsx'
    sheetname = 'Subscribers & Equipment'
    writer = pd.ExcelWriter(filename, engine = 'xlsxwriter')
    df.to_excel(writer, sheet_name = sheetname, header = False, index = False)
    worksheet = writer.sheets[sheetname]
    (max_row, max_col) = df.shape
    headers = [{'header': header } for header in df.columns]
    worksheet.add_table(0, 0, max_row - 1, max_col - 1, {'columns': headers})
    writer.save()
    print('\t - Finished.')

def trial_3(login_info): # Looks for charges without payments
    dsn_tns = cx_Oracle.makedsn('ora-tns-qcc1.in.qservco.com', 1521, service_name = 'qcc1' )
    connection = cx_Oracle.connect(
        user = login_info[0],
        password = login_info[1],
        dsn = dsn_tns)
    print('='*60)
    print('\t - Connection established.')
    query = '''
select distinct
    s.sub_id, s.sub_nm, to_char(invoice.trans_dttm, 'YYYY-MM-DD') as invoice_dt,
    invoice.amt as invoice_sum_amt,
    listagg(invoice.trans_nm, '; ') as transactions
from
    (
        select
            max(trans_dttm) as trans_dttm, sum(amt) as amt,
            trans_nm, sub_id
        from wasabi.v_trans t,
        (
            select
                trans_typ, trans_nm
            from wasabi.v_trans_typ
            where lower(trans_nm) like '%equip%nrc%'
        ) nm
        where t.trans_cls = 'R'
            and t.amt > 0
            and (t.trans_stat = 'I' or t.trans_stat = 'C')
            and t.trans_dttm >= add_months(trunc(sysdate), -6)
            and t.trans_typ in nm.trans_typ
        group by trans_nm, sub_id, trans_cls
    ) invoice, wasabi.v_sub s
where invoice.sub_id = s.sub_id
and not exists (
        select
            null
        from wasabi.v_trans
        where trans_cls = 'P'
            and (trans_stat = 'I' or trans_stat = 'C')
            and sub_id = invoice.sub_id
            and trans_dttm >= invoice.trans_dttm
    )
group by s.sub_id, s.sub_nm, invoice.trans_dttm, invoice.amt, invoice.trans_nm
    '''
    df = pd.read_sql(query, connection)
    print('\t - Read sql.')
    filename = 'Billed_Equipment_Not_Paid_6mo.xlsx'
    sheetname = 'Subscribers & Equipment'
    writer = pd.ExcelWriter(filename, engine = 'xlsxwriter')
    df.to_excel(writer, sheet_name = sheetname, header = False, index = False)
    worksheet = writer.sheets[sheetname]
    (max_row, max_col) = df.shape
    headers = [{'header': header } for header in df.columns]
    worksheet.add_table(0, 0, max_row - 1, max_col - 1, {'columns': headers, 'style': 'Table Style Dark 5'})
    writer.save()
    print('\t - Finished.')

t1 = timeit.Timer('trial_1(login_info)', 'from __main__ import trial_1, login_info').timeit(number=1)
#t2 = timeit.Timer('trial_2(login_info)', 'from __main__ import trial_2, login_info').timeit(number=1)
t3 = timeit.Timer('trial_3(login_info)', 'from __main__ import trial_3, login_info').timeit(number=1)

print('+'*60)
print(f'\t - Trial 1 took {t1} seconds.')
# print(f'\t - Trial 2 took {t2} seconds.')
print(f'\t - Trial 3 took {t3} seconds.')
print('='*60)
