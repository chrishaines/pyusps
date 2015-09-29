import requests_mock

from collections import OrderedDict
from nose.tools import eq_ as eq

from pyusps.address_information import verify
from pyusps.test.util import assert_raises, assert_errors_equal


@requests_mock.mock()
def test_verify_simple(m):
    req = """http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=%3CAddressValidateRequest+USERID%3D%22foo_id%22%3E%3CAddress+ID%3D%220%22%3E%3CAddress1%2F%3E%3CAddress2%3E6406+Ivy+Lane%3C%2FAddress2%3E%3CCity%3EGreenbelt%3C%2FCity%3E%3CState%3EMD%3C%2FState%3E%3CZip5%3E20770%3C%2FZip5%3E%3CZip4%3E%3C%2FZip4%3E%3C%2FAddress%3E%3C%2FAddressValidateRequest%3E"""

    s = """<?xml version="1.0"?>
<AddressValidateResponse><Address ID="0"><Address2>6406 IVY LN</Address2><City>GREENBELT</City><State>MD</State><Zip5>20770</Zip5><Zip4>1441</Zip4></Address></AddressValidateResponse>"""
    m.get(req, text=s)

    address = OrderedDict([
            ('address', '6406 Ivy Lane'),
            ('city', 'Greenbelt'),
            ('state', 'MD'),
            ('zip_code', '20770'),
            ])
    res = verify('foo_id', address)
    eq(1, m.called)

    expected = OrderedDict([
            ('address', '6406 IVY LN'),
            ('city', 'GREENBELT'),
            ('state', 'MD'),
            ('zip5', '20770'),
            ('zip4', '1441'),
            ])
    eq(res, expected)


@requests_mock.mock()
def test_verify_zip5(m):
    req = """http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=%3CAddressValidateRequest+USERID%3D%22foo_id%22%3E%3CAddress+ID%3D%220%22%3E%3CAddress1%2F%3E%3CAddress2%3E6406+Ivy+Lane%3C%2FAddress2%3E%3CCity%3EGreenbelt%3C%2FCity%3E%3CState%3EMD%3C%2FState%3E%3CZip5%3E20770%3C%2FZip5%3E%3CZip4%3E%3C%2FZip4%3E%3C%2FAddress%3E%3C%2FAddressValidateRequest%3E"""
    res = ("""<?xml version="1.0"?>
<AddressValidateResponse><Address ID="0"><Address2>6406 IVY LN</Address2><City>GREENBELT</City><State>MD</State><Zip5>20770</Zip5><Zip4>1441</Zip4></Address></AddressValidateResponse>""")
    m.get(req, text=res, complete_qs=True)

    address = OrderedDict([
            ('address', '6406 Ivy Lane'),
            ('city', 'Greenbelt'),
            ('state', 'MD'),
            ('zip_code', '20770'),
            ])
    res = verify('foo_id', address)
    eq(1, m.called)

    expected = OrderedDict([
            ('address', '6406 IVY LN'),
            ('city', 'GREENBELT'),
            ('state', 'MD'),
            ('zip5', '20770'),
            ('zip4', '1441'),
            ])
    eq(res, expected)


@requests_mock.mock()
def test_verify_zip_both(m):
    req = """http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=%3CAddressValidateRequest+USERID%3D%22foo_id%22%3E%3CAddress+ID%3D%220%22%3E%3CAddress1%2F%3E%3CAddress2%3E6406+Ivy+Lane%3C%2FAddress2%3E%3CCity%3EGreenbelt%3C%2FCity%3E%3CState%3EMD%3C%2FState%3E%3CZip5%3E20770%3C%2FZip5%3E%3CZip4%3E1441%3C%2FZip4%3E%3C%2FAddress%3E%3C%2FAddressValidateRequest%3E"""
    res = ("""<?xml version="1.0"?>
<AddressValidateResponse><Address ID="0"><Address2>6406 IVY LN</Address2><City>GREENBELT</City><State>MD</State><Zip5>20770</Zip5><Zip4>1441</Zip4></Address></AddressValidateResponse>""")
    m.get(req, text=res, complete_qs=True)

    address = OrderedDict([
            ('address', '6406 Ivy Lane'),
            ('city', 'Greenbelt'),
            ('state', 'MD'),
            ('zip_code', '207701441'),
            ])
    res = verify('foo_id', address)
    eq(1, m.called)

    expected = OrderedDict([
            ('address', '6406 IVY LN'),
            ('city', 'GREENBELT'),
            ('state', 'MD'),
            ('zip5', '20770'),
            ('zip4', '1441'),
            ])
    eq(res, expected)


@requests_mock.mock()
def test_verify_zip_dash(m):
    req = """http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=%3CAddressValidateRequest+USERID%3D%22foo_id%22%3E%3CAddress+ID%3D%220%22%3E%3CAddress1%2F%3E%3CAddress2%3E6406+Ivy+Lane%3C%2FAddress2%3E%3CCity%3EGreenbelt%3C%2FCity%3E%3CState%3EMD%3C%2FState%3E%3CZip5%3E20770%3C%2FZip5%3E%3CZip4%3E1441%3C%2FZip4%3E%3C%2FAddress%3E%3C%2FAddressValidateRequest%3E"""
    res = ("""<?xml version="1.0"?>
<AddressValidateResponse><Address ID="0"><Address2>6406 IVY LN</Address2><City>GREENBELT</City><State>MD</State><Zip5>20770</Zip5><Zip4>1441</Zip4></Address></AddressValidateResponse>""")
    m.get(req, text=res, complete_qs=True)

    address = OrderedDict([
            ('address', '6406 Ivy Lane'),
            ('city', 'Greenbelt'),
            ('state', 'MD'),
            ('zip_code', '20770-1441'),
            ])
    res = verify('foo_id', address)
    eq(1, m.called)

    expected = OrderedDict([
            ('address', '6406 IVY LN'),
            ('city', 'GREENBELT'),
            ('state', 'MD'),
            ('zip5', '20770'),
            ('zip4', '1441'),
            ])
    eq(res, expected)


@requests_mock.mock()
def test_verify_zip_only(m):
    req = """http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=%3CAddressValidateRequest+USERID%3D%22foo_id%22%3E%3CAddress+ID%3D%220%22%3E%3CAddress1%2F%3E%3CAddress2%3E6406+Ivy+Lane%3C%2FAddress2%3E%3CCity%3EGreenbelt%3C%2FCity%3E%3CState%2F%3E%3CZip5%3E20770%3C%2FZip5%3E%3CZip4%3E%3C%2FZip4%3E%3C%2FAddress%3E%3C%2FAddressValidateRequest%3E"""
    res = ("""<?xml version="1.0"?>
<AddressValidateResponse><Address ID="0"><Address2>6406 IVY LN</Address2><City>GREENBELT</City><State>MD</State><Zip5>20770</Zip5><Zip4>1441</Zip4></Address></AddressValidateResponse>""")
    m.get(req, text=res, complete_qs=True)

    address = OrderedDict([
            ('address', '6406 Ivy Lane'),
            ('city', 'Greenbelt'),
            ('zip_code', '20770'),
            ])
    res = verify('foo_id', address)
    eq(1, m.called)

    expected = OrderedDict([
            ('address', '6406 IVY LN'),
            ('city', 'GREENBELT'),
            ('state', 'MD'),
            ('zip5', '20770'),
            ('zip4', '1441'),
            ])
    eq(res, expected)


@requests_mock.mock()
def test_verify_state_only(m):
    req = """http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=%3CAddressValidateRequest+USERID%3D%22foo_id%22%3E%3CAddress+ID%3D%220%22%3E%3CAddress1%2F%3E%3CAddress2%3E6406+Ivy+Lane%3C%2FAddress2%3E%3CCity%3EGreenbelt%3C%2FCity%3E%3CState%3EMD%3C%2FState%3E%3CZip5%2F%3E%3CZip4%2F%3E%3C%2FAddress%3E%3C%2FAddressValidateRequest%3E"""
    res = ("""<?xml version="1.0"?>
<AddressValidateResponse><Address ID="0"><Address2>6406 IVY LN</Address2><City>GREENBELT</City><State>MD</State><Zip5>20770</Zip5><Zip4>1441</Zip4></Address></AddressValidateResponse>""")
    m.get(req, text=res, complete_qs=True)

    address = OrderedDict([
            ('address', '6406 Ivy Lane'),
            ('city', 'Greenbelt'),
            ('state', 'MD'),
            ])
    res = verify('foo_id', address)
    eq(1, m.called)

    expected = OrderedDict([
            ('address', '6406 IVY LN'),
            ('city', 'GREENBELT'),
            ('state', 'MD'),
            ('zip5', '20770'),
            ('zip4', '1441'),
            ])
    eq(res, expected)


@requests_mock.mock()
def test_verify_firm_name(m):
    req = """http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=%3CAddressValidateRequest+USERID%3D%22foo_id%22%3E%3CAddress+ID%3D%220%22%3E%3CFirmName%3EXYZ+Corp%3C%2FFirmName%3E%3CAddress1%2F%3E%3CAddress2%3E6406+Ivy+Lane%3C%2FAddress2%3E%3CCity%3EGreenbelt%3C%2FCity%3E%3CState%3EMD%3C%2FState%3E%3CZip5%2F%3E%3CZip4%2F%3E%3C%2FAddress%3E%3C%2FAddressValidateRequest%3E"""
    res = ("""<?xml version="1.0"?>
<AddressValidateResponse><Address ID="0"><FirmName>XYZ CORP</FirmName><Address2>6406 IVY LN</Address2><City>GREENBELT</City><State>MD</State><Zip5>20770</Zip5><Zip4>1441</Zip4></Address></AddressValidateResponse>""")
    m.get(req, text=res, complete_qs=True)

    address = OrderedDict([
            ('firm_name', 'XYZ Corp'),
            ('address', '6406 Ivy Lane'),
            ('city', 'Greenbelt'),
            ('state', 'MD'),
            ])
    res = verify('foo_id', address)
    eq(1, m.called)

    expected = OrderedDict([
            ('firm_name', 'XYZ CORP'),
            ('address', '6406 IVY LN'),
            ('city', 'GREENBELT'),
            ('state', 'MD'),
            ('zip5', '20770'),
            ('zip4', '1441'),
            ])
    eq(res, expected)


@requests_mock.mock()
def test_verify_address_extended(m):
    req = """http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=%3CAddressValidateRequest+USERID%3D%22foo_id%22%3E%3CAddress+ID%3D%220%22%3E%3CAddress1%3ESuite+12%3C%2FAddress1%3E%3CAddress2%3E6406+Ivy+Lane%3C%2FAddress2%3E%3CCity%3EGreenbelt%3C%2FCity%3E%3CState%3EMD%3C%2FState%3E%3CZip5%2F%3E%3CZip4%2F%3E%3C%2FAddress%3E%3C%2FAddressValidateRequest%3E"""
    res = ("""<?xml version="1.0"?>
<AddressValidateResponse><Address ID="0"><Address1>STE 12</Address1><Address2>6406 IVY LN</Address2><City>GREENBELT</City><State>MD</State><Zip5>20770</Zip5><Zip4>1441</Zip4></Address></AddressValidateResponse>""")
    m.get(req, text=res, complete_qs=True)

    address = OrderedDict([
            ('address', '6406 Ivy Lane'),
            ('address_extended', 'Suite 12'),
            ('city', 'Greenbelt'),
            ('state', 'MD'),
            ])
    res = verify('foo_id', address)
    eq(1, m.called)

    expected = OrderedDict([
            ('address_extended', 'STE 12'),
            ('address', '6406 IVY LN'),
            ('city', 'GREENBELT'),
            ('state', 'MD'),
            ('zip5', '20770'),
            ('zip4', '1441'),
            ])
    eq(res, expected)


@requests_mock.mock()
def test_verify_urbanization(m):
    req = """http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=%3CAddressValidateRequest+USERID%3D%22foo_id%22%3E%3CAddress+ID%3D%220%22%3E%3CAddress1%2F%3E%3CAddress2%3E6406+Ivy+Lane%3C%2FAddress2%3E%3CCity%3EGreenbelt%3C%2FCity%3E%3CState%3EMD%3C%2FState%3E%3CUrbanization%3EPuerto+Rico%3C%2FUrbanization%3E%3CZip5%2F%3E%3CZip4%2F%3E%3C%2FAddress%3E%3C%2FAddressValidateRequest%3E"""
    res = ("""<?xml version="1.0"?>
<AddressValidateResponse><Address ID="0"><Address2>6406 IVY LN</Address2><City>GREENBELT</City><State>MD</State><Urbanization>PUERTO RICO</Urbanization><Zip5>20770</Zip5><Zip4>1441</Zip4></Address></AddressValidateResponse>""")

    m.get(req, text=res, complete_qs=True)

    address = OrderedDict([
            ('address', '6406 Ivy Lane'),
            ('urbanization', 'Puerto Rico'),
            ('city', 'Greenbelt'),
            ('state', 'MD'),
            ])
    res = verify('foo_id', address)
    eq(1, m.called)

    expected = OrderedDict([
            ('address', '6406 IVY LN'),
            ('city', 'GREENBELT'),
            ('state', 'MD'),
            ('urbanization', 'PUERTO RICO'),
            ('zip5', '20770'),
            ('zip4', '1441'),
            ])
    eq(res, expected)


@requests_mock.mock()
def test_verify_multiple(m):
    req = """http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=%3CAddressValidateRequest+USERID%3D%22foo_id%22%3E%3CAddress+ID%3D%220%22%3E%3CAddress1%2F%3E%3CAddress2%3E6406+Ivy+Lane%3C%2FAddress2%3E%3CCity%3EGreenbelt%3C%2FCity%3E%3CState%3EMD%3C%2FState%3E%3CZip5%2F%3E%3CZip4%2F%3E%3C%2FAddress%3E%3CAddress+ID%3D%221%22%3E%3CAddress1%2F%3E%3CAddress2%3E8+Wildwood+Drive%3C%2FAddress2%3E%3CCity%3EOld+Lyme%3C%2FCity%3E%3CState%3ECT%3C%2FState%3E%3CZip5%2F%3E%3CZip4%2F%3E%3C%2FAddress%3E%3C%2FAddressValidateRequest%3E"""
    res = ("""<?xml version="1.0"?>
<AddressValidateResponse><Address ID="0"><Address2>6406 IVY LN</Address2><City>GREENBELT</City><State>MD</State><Zip5>20770</Zip5><Zip4>1441</Zip4></Address><Address ID="1"><Address2>8 WILDWOOD DR</Address2><City>OLD LYME</City><State>CT</State><Zip5>06371</Zip5><Zip4>1844</Zip4></Address></AddressValidateResponse>""")
    m.get(req, text=res, complete_qs=True)

    addresses = [
        OrderedDict([
                ('address', '6406 Ivy Lane'),
                ('city', 'Greenbelt'),
                ('state', 'MD'),
                ]),
        OrderedDict([
                ('address', '8 Wildwood Drive'),
                ('city', 'Old Lyme'),
                ('state', 'CT'),
                ]),
        ]
    res = verify('foo_id', *addresses)
    eq(1, m.called)

    expected = [
        OrderedDict([
                ('address', '6406 IVY LN'),
                ('city', 'GREENBELT'),
                ('state', 'MD'),
                ('zip5', '20770'),
                ('zip4', '1441'),
                ]),
        OrderedDict([
                ('address', '8 WILDWOOD DR'),
                ('city', 'OLD LYME'),
                ('state', 'CT'),
                ('zip5', '06371'),
                ('zip4', '1844'),
                ]),
        ]
    eq(res, expected)


def test_verify_more_than_5():
    addresses = [
        OrderedDict(),
        OrderedDict(),
        OrderedDict(),
        OrderedDict(),
        OrderedDict(),
        OrderedDict(),
        ]

    msg = assert_raises(
        ValueError,
        verify,
        'foo_id',
        *addresses
        )

    eq(str(msg), 'Only 5 addresses are allowed per request')


@requests_mock.mock()
def test_verify_api_root_error(m):
    req = """http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=%3CAddressValidateRequest+USERID%3D%22foo_id%22%3E%3CAddress+ID%3D%220%22%3E%3CAddress1%2F%3E%3CAddress2%3E6406+Ivy+Lane%3C%2FAddress2%3E%3CCity%3EGreenbelt%3C%2FCity%3E%3CState%3EMD%3C%2FState%3E%3CZip5%2F%3E%3CZip4%2F%3E%3C%2FAddress%3E%3C%2FAddressValidateRequest%3E"""
    res = ("""<Error>
        <Number>80040b1a</Number>
        <Description>Authorization failure.  Perhaps username and/or password is incorrect.</Description>
        <Source>UspsCom::DoAuth</Source>
</Error>""")
    m.get(req, text=res, complete_qs=True)

    address = OrderedDict([
            ('address', '6406 Ivy Lane'),
            ('city', 'Greenbelt'),
            ('state', 'MD'),
            ])
    msg = assert_raises(
        ValueError,
        verify,
        'foo_id',
        address
        )
    eq(1, m.called)

    expected = ('80040b1a: Authorization failure.  Perhaps username '
                'and/or password is incorrect.'
                )
    eq(str(msg), expected)


@requests_mock.mock()
def test_verify_api_address_error_single(m):
    req = """http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=%3CAddressValidateRequest+USERID%3D%22foo_id%22%3E%3CAddress+ID%3D%220%22%3E%3CAddress1%2F%3E%3CAddress2%3E6406+Ivy+Lane%3C%2FAddress2%3E%3CCity%3EGreenbelt%3C%2FCity%3E%3CState%3ENJ%3C%2FState%3E%3CZip5%2F%3E%3CZip4%2F%3E%3C%2FAddress%3E%3C%2FAddressValidateRequest%3E"""
    res =   ("""<?xml version="1.0"?>
<AddressValidateResponse><Address ID="0"><Error><Number>-2147219401</Number><Source>API_AddressCleancAddressClean.CleanAddress2;SOLServer.CallAddressDll</Source><Description>Address Not Found.</Description><HelpFile></HelpFile><HelpContext>1000440</HelpContext></Error></Address></AddressValidateResponse>""")
    m.get(req, text=res, complete_qs=True)

    address = OrderedDict([
            ('address', '6406 Ivy Lane'),
            ('city', 'Greenbelt'),
            ('state', 'NJ'),
            ])
    msg = assert_raises(
        ValueError,
        verify,
        'foo_id',
        address
        )
    eq(1, m.called)

    expected = '-2147219401: Address Not Found.'
    eq(str(msg), expected)


@requests_mock.mock()
def test_verify_api_address_error_multiple(m):
    req = """http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=%3CAddressValidateRequest+USERID%3D%22foo_id%22%3E%3CAddress+ID%3D%220%22%3E%3CAddress1%2F%3E%3CAddress2%3E6406+Ivy+Lane%3C%2FAddress2%3E%3CCity%3EGreenbelt%3C%2FCity%3E%3CState%3EMD%3C%2FState%3E%3CZip5%2F%3E%3CZip4%2F%3E%3C%2FAddress%3E%3CAddress+ID%3D%221%22%3E%3CAddress1%2F%3E%3CAddress2%3E8+Wildwood+Drive%3C%2FAddress2%3E%3CCity%3EOld+Lyme%3C%2FCity%3E%3CState%3ENJ%3C%2FState%3E%3CZip5%2F%3E%3CZip4%2F%3E%3C%2FAddress%3E%3C%2FAddressValidateRequest%3E"""
    res = ("""<?xml version="1.0"?>
<AddressValidateResponse><Address ID="0"><Address2>6406 IVY LN</Address2><City>GREENBELT</City><State>MD</State><Zip5>20770</Zip5><Zip4>1441</Zip4></Address><Address ID="1"><Error><Number>-2147219400</Number><Source>API_AddressCleancAddressClean.CleanAddress2;SOLServer.CallAddressDll</Source><Description>Invalid City.</Description><HelpFile></HelpFile><HelpContext>1000440</HelpContext></Error></Address></AddressValidateResponse>""")
    m.get(req, text=res, complete_qs=True)

    addresses = [
        OrderedDict([
                ('address', '6406 Ivy Lane'),
                ('city', 'Greenbelt'),
                ('state', 'MD'),
                ]),
        OrderedDict([
                ('address', '8 Wildwood Drive'),
                ('city', 'Old Lyme'),
                ('state', 'NJ'),
                ]),
        ]
    res = verify('foo_id', *addresses)
    eq(1, m.called)

    # eq does not work with exceptions. Process each item manually.
    eq(len(res), 2)
    eq(
        res[0],
        OrderedDict([
                ('address', '6406 IVY LN'),
                ('city', 'GREENBELT'),
                ('state', 'MD'),
                ('zip5', '20770'),
                ('zip4', '1441'),
                ]),
       )
    assert_errors_equal(
        res[1],
        ValueError('-2147219400: Invalid City.'),
        )


@requests_mock.mock()
def test_verify_api_empty_error(m):
    req = """http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=%3CAddressValidateRequest+USERID%3D%22foo_id%22%3E%3CAddress+ID%3D%220%22%3E%3CAddress1%2F%3E%3CAddress2%3E6406+Ivy+Lane%3C%2FAddress2%3E%3CCity%3EGreenbelt%3C%2FCity%3E%3CState%3ENJ%3C%2FState%3E%3CZip5%2F%3E%3CZip4%2F%3E%3C%2FAddress%3E%3C%2FAddressValidateRequest%3E"""
    res = ("""<?xml version="1.0"?>
<AddressValidateResponse></AddressValidateResponse>""")
    m.get(req, text=res, complete_qs=True)

    address = OrderedDict([
            ('address', '6406 Ivy Lane'),
            ('city', 'Greenbelt'),
            ('state', 'NJ'),
            ])
    msg = assert_raises(
        TypeError,
        verify,
        'foo_id',
        address
        )
    eq(1, m.called)

    expected = 'Could not find any address or error information'
    eq(str(msg), expected)


@requests_mock.mock()
def test_verify_api_order_error(m):
    req = """http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=%3CAddressValidateRequest+USERID%3D%22foo_id%22%3E%3CAddress+ID%3D%220%22%3E%3CAddress1%2F%3E%3CAddress2%3E6406+Ivy+Lane%3C%2FAddress2%3E%3CCity%3EGreenbelt%3C%2FCity%3E%3CState%3EMD%3C%2FState%3E%3CZip5%2F%3E%3CZip4%2F%3E%3C%2FAddress%3E%3CAddress+ID%3D%221%22%3E%3CAddress1%2F%3E%3CAddress2%3E8+Wildwood+Drive%3C%2FAddress2%3E%3CCity%3EOld+Lyme%3C%2FCity%3E%3CState%3ECT%3C%2FState%3E%3CZip5%2F%3E%3CZip4%2F%3E%3C%2FAddress%3E%3C%2FAddressValidateRequest%3E"""
    res = ("""<?xml version="1.0"?>
<AddressValidateResponse><Address ID="0"><Address2>6406 IVY LN</Address2><City>GREENBELT</City><State>MD</State><Zip5>20770</Zip5><Zip4>1441</Zip4></Address><Address ID="2"><Address2>8 WILDWOOD DR</Address2><City>OLD LYME</City><State>CT</State><Zip5>06371</Zip5><Zip4>1844</Zip4></Address></AddressValidateResponse>""")
    m.get(req, text=res, complete_qs=True)

    addresses = [
        OrderedDict([
                ('address', '6406 Ivy Lane'),
                ('city', 'Greenbelt'),
                ('state', 'MD'),
                ]),
        OrderedDict([
                ('address', '8 Wildwood Drive'),
                ('city', 'Old Lyme'),
                ('state', 'CT'),
                ]),
        ]
    msg = assert_raises(
        IndexError,
        verify,
        'foo_id',
        *addresses
        )
    eq(1, m.called)

    expected = ('The addresses returned are not in the same order '
                'they were requested'
                )
    eq(str(msg), expected)
