import aiohttp
import asyncio
import time

start_time = time.time()


async def get_text(session, url):
    async with session.get(url) as resp:
        text = await resp.text()
        return text


async def main():

    async with aiohttp.ClientSession() as session:
        tasks = []
        job_urls = [
            'http://vercel.com/careers/analytics-engineer-amer-4486497004',
            'http://vercel.com/careers/application-security-engineer-us-4626993004',
            'http://vercel.com/careers/content-engineer-us-4534477004',
            'http://vercel.com/careers/customer-success-manager-apac-4159182004',
            'http://vercel.com/careers/customer-success-manager-europe-uk-4215448004',
            'http://vercel.com/careers/data-engineer-uk-us-4664444004',
            'http://vercel.com/careers/data-engineer-europe-uk-us-4674120004',
            'http://vercel.com/careers/data-scientist-us-4554464004',
            'http://vercel.com/careers/director-commercial-legal-us-4505262004',
            'http://vercel.com/careers/director-of-revenue-marketing-us-4675158004',
            'http://vercel.com/careers/engineering-manager-edge-network-us-4534415004',
            'http://vercel.com/careers/engineering-manager-turborepo-us-4531844004',
            'http://vercel.com/careers/enterprise-account-executive-apac-4346323004',
            'http://vercel.com/careers/enterprise-account-executive-europe-uk-4235041004',
            'http://vercel.com/careers/field-marketing-manager-west-us-4623565004',
            'http://vercel.com/careers/financial-systems-analyst-us-4668362004',
            'http://vercel.com/careers/head-of-business-operations-us-4657870004',
            'http://vercel.com/careers/infrastructure-engineer-us-4159198004',
            'http://vercel.com/careers/instructional-designer-europe-uk-us-4651728004',
            'http://vercel.com/careers/mid-market-account-executive-apac-4466236004',
            'http://vercel.com/careers/mid-market-account-executive-europe-uk-4180390004',
            'http://vercel.com/careers/multimedia-designer-us-4677077004',
            'http://vercel.com/careers/partner-manager-services-apac-4553099004',
            'http://vercel.com/careers/partner-manager-services-europe-uk-4502534004',
            'http://vercel.com/careers/product-advocate-us-4558502004',
            'http://vercel.com/careers/product-manager-usage-and-billing-us-4327432004',
            'http://vercel.com/careers/sales-development-lead-apac-4423850004',
            'http://vercel.com/careers/sales-development-representative-enterprise-us-4586706004',
            'http://vercel.com/careers/sales-development-representative-enterprise-europe-uk-4646256004',
            'http://vercel.com/careers/sales-development-representative-manager-east-us-4581381004',
            'http://vercel.com/careers/sales-development-representative-mid-market-us-4414553004',
            'http://vercel.com/careers/sales-engineer-us-4162371004',
            'http://vercel.com/careers/sales-engineer-apac-4159197004',
            'http://vercel.com/careers/sales-engineer-europe-uk-4182467004',
            'http://vercel.com/careers/salesforce-administrator-us-4606272004',
            'http://vercel.com/careers/senior-manager-customer-success-management-us-4426201004',
            'http://vercel.com/careers/senior-manager-trust-and-safety-us-4431286004',
            'http://vercel.com/careers/senior-marketing-operations-manager-us-4625781004',
            'http://vercel.com/careers/senior-product-manager-collaboration-us-4486791004',
            'http://vercel.com/careers/senior-product-manager-next-js-europe-uk-4434286004',
            'http://vercel.com/careers/senior-product-manager-turborepo-us-4547564004',
            'http://vercel.com/careers/senior-visual-web-designer-us-4376536004',
            'http://vercel.com/careers/software-engineer-observability-europe-uk-4531506004',
            'http://vercel.com/careers/software-engineer-support-tools-uk-us-4641478004',
            'http://vercel.com/careers/software-engineer-systems-us-4656326004',
            'http://vercel.com/careers/solutions-engineer-us-4553561004',
            'http://vercel.com/careers/solutions-engineer-europe-uk-4159200004',
            'http://vercel.com/careers/solutions-engineer-partnerships-us-4553614004',
            'http://vercel.com/careers/staff-software-engineer-systems-us-4652493004',
            'http://vercel.com/careers/technical-enablement-lead-europe-uk-4598745004',
            'http://vercel.com/careers/technical-inbound-sales-lead-europe-uk-4603098004',
            'http://vercel.com/careers/vercel-general-application-uk-us-4569242004',
            'http://vercel.com/careers/vice-president-gtm-operations-us-4436899004',
            'http://vercel.com/careers/visual-designer-brand-marketing-us-4536670004'
        ]
        for url in job_urls:
            tasks.append(asyncio.ensure_future(get_text(session, url)))

        job_htmls = await asyncio.gather(*tasks)
        for html in job_htmls:
            print(html[0:100])

asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))

# import aiohttp
# import asyncio
# import time

# start_time = time.time()


# async def get_pokemon(session, url):
#     async with session.get(url) as resp:
#         pokemon = await resp.json()
#         return pokemon


# async def main():

#     async with aiohttp.ClientSession() as session:

#         tasks = []
#         for number in range(1, 151):
#             url = f'https://pokeapi.co/api/v2/pokemon/{number}'
#             tasks.append(asyncio.ensure_future(get_pokemon(session, url)))

#         original_pokemon = await asyncio.gather(*tasks)
#         for pokemon in original_pokemon:
#             print(pokemon)

# asyncio.run(main())
# print("--- %s seconds ---" % (time.time() - start_time))