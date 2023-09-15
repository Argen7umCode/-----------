import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from pprint import pprint
from urllib import request

# mp = MultipartEncoder(fields={
#     "maxSum" : "0",
#     "PageNumber" : "2",62300647301660366405
#     "IsGosContract" : "False",
#     "ActivityDirectionId" : "1"
# })

req = requests.post(url=" http://rating.nopriz.ru/Home/GetFilteredList",
                    files=(
                        ("PageNumber", (None, 2)),
                        ("ActivityDirectionId", (None, 1))
                    ))

pprint(req.json())


# url = 'https://open-api.egrz.ru/api/PublicRegistrationBook/openDataFile?$filter=(contains(tolower(ExpertiseOrganizatioInfo),tolower(%3442112404))%20or%20contains(tolower(ExpertiseNumber),tolower(%3442112404))%20or%20contains(tolower(WorkType),tolower(%3442112404))%20or%20contains(tolower(ExpertiseResultType),tolower(%3442112404))%20or%20contains(tolower(ExpertiseType),tolower(%3442112404))%20or%20contains(tolower(ExpertiseDocumentType),tolower(%3442112404))%20or%20contains(tolower(ExpertiseObjectNameAndAddress),tolower(%3442112404))%20or%20contains(tolower(EconomyEfficiencyInfo),tolower(%3442112404))%20or%20contains(tolower(PreviousExpretiseResults),tolower(%3442112404))%20or%20contains(tolower(DeveloperAndTechnicalCustomerOrganizationInfo),tolower(%3442112404))%20or%20contains(tolower(PlannerOrganizationInfo),tolower(%3442112404))%20or%20contains(tolower(SubjectRf),tolower(%3442112404)))&$orderby=ExpertiseDate%20desc%20&$count=true&$top=5&$skip=0'
# r = requests.get(url)
# pprint(r.text)

