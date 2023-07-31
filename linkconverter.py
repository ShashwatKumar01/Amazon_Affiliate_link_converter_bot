from urllib.parse import urlparse, parse_qs, urlunparse
import requests

def unshorten_url(short_url):
    try:
        response = requests.head(short_url, allow_redirects=True)
        return response.url
    except requests.exceptions.RequestException:
        return None

def remove_amazon_affiliate_parameters(url):
    parsed_url = urlparse(url)
    # print(parsed_url)
    query_params = parse_qs(parsed_url.query)
    # print(query_params)

    # List of Amazon affiliate parameters to remove
    amazon_affiliate_params = ['tag', 'ref', 'linkCode', 'camp', 'creative','linkId','ref_','language','content-id','_encoding']

    # Remove the Amazon affiliate parameters from the query parameters
    cleaned_query_params = {key: value for key, value in query_params.items() if key not in amazon_affiliate_params}

    # Rebuild the URL with the cleaned query parameters
    cleaned_url = urlunparse(parsed_url._replace(query='&'.join([f'{key}={value[0]}' for key, value in cleaned_query_params.items()])))

    return cleaned_url

def create_amazon_affiliate_url(normal_url, affiliate_tag):
    if "amazon" not in normal_url:
        return "Not a valid Amazon link."

    if not affiliate_tag:
        return "Please provide a valid affiliate tag."

    # Check if the URL already has query parameters
    separator = '&' if '?' in normal_url else '?'

    # Append the affiliate tag to the URL
    affiliate_url = f"{normal_url}{separator}tag={affiliate_tag}"

    return affiliate_url

def shorten_url_with_tinyurl(long_url):
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={long_url}")
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to shorten URL.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:


# short_url = input("Enter Shortened Url ")
# affiliate_tag = "highfivesto0c-21"
#
# unshortened_url = unshorten_url(short_url)
# print("Unshortened URL:", unshortened_url)
#
# affiliate_url = unshortened_url
# cleaned_url = remove_amazon_affiliate_parameters(affiliate_url)
# print("Cleaned URL:", cleaned_url)
#
# affiliate_url = create_amazon_affiliate_url(cleaned_url, affiliate_tag)
# print("Affiliate URL:", affiliate_url)
#
# long_url = affiliate_url
# short_url = shorten_url_with_tinyurl(long_url)
# print("Shortened URL:", short_url)
