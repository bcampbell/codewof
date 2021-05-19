import datetime
from enum import Enum

from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone
from users.models import User
from programming.models import Attempt
from utils.Weekday import Weekday


class Command(BaseCommand):
    """Required command class for the custom Django load_user_types command."""

    # Email body html. Split into two parts so a custom message can be inserted between <p> tags.
    # TODO Do this better using https://stackoverflow.com/questions/2809547/creating-email-templates-with-django and replace hardcoded urls
    email_first_half = """
    <!DOCTYPE html>
    <!-- Set the language of your main document. This helps screenreaders use the proper language profile, pronunciation, and accent. -->
    <html lang="en">
    <head>
        <!-- The title is useful for screenreaders reading a document. Use your sender name or subject line. -->
        <title>An Accessible Email</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <!-- Never disable zoom behavior! Fine to set the initial width and scale, but allow users to set their own zoom preferences. -->
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <style>
            /* CLIENT-SPECIFIC STYLES */
            body, table, td, a { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
            table, td { mso-table-lspace: 0; mso-table-rspace: 0; }
            img { -ms-interpolation-mode: bicubic; }

            /* RESET STYLES */
            img { border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }
            table { border-collapse: collapse !important; }
            body { height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; }

            /* iOS BLUE LINKS */
            a[x-apple-data-detectors] {
                color: inherit !important;
                text-decoration: none !important;
                font-size: inherit !important;
                font-family: inherit !important;
                font-weight: inherit !important;
                line-height: inherit !important;
            }

            /* GMAIL BLUE LINKS */
            u + #body a {
                color: inherit;
                text-decoration: none;
                font-size: inherit;
                font-family: inherit;
                font-weight: inherit;
                line-height: inherit;
            }

            /* SAMSUNG MAIL BLUE LINKS */
            #MessageViewBody a {
                color: inherit;
                text-decoration: none;
                font-size: inherit;
                font-family: inherit;
                font-weight: inherit;
                line-height: inherit;
            }

            /* These rules set the link and hover states, making it clear that links are, in fact, links. */
            /* Embrace established conventions like underlines on links to keep emails accessible. */
            a { color: #B200FD; font-weight: 600; text-decoration: underline; }
            a:hover { color: #000000 !important; text-decoration: none !important; }

            /* These rules adjust styles for desktop devices, keeping the email responsive for users. */
            /* Some email clients don't properly apply media query-based styles, which is why we go mobile-first. */
            @media screen and (min-width:600px) {
                h1 { font-size: 48px !important; line-height: 48px !important; }
                .intro { font-size: 24px !important; line-height: 36px !important; }
            }
        </style>
    </head>
    <body style="margin: 0 !important; padding: 0 !important;">

    <!-- Some preview text. -->
    <div style="display: none; max-height: 0; overflow: hidden;">

    </div>
    <!-- Get rid of unwanted preview text. -->
    <div style="display: none; max-height: 0; overflow: hidden;">
        &nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;
    </div>

    <!-- This ghost table is used to constrain the width in Outlook. The role attribute is set to presentation to prevent it from being read by screenreaders. -->
    <!--[if (gte mso 9)|(IE)]>
    <table role="presentation"><tr><td>
    <![endif]-->
    <!-- The role and aria-label attributes are added to wrap the email content as an article for screen readers. Some of them will read out the aria-label as the title of the document, so use something like "An email from Your Brand Name" to make it recognizable. -->
    <!-- Default styling of text is applied to the wrapper div. Be sure to use text that is large enough and has a high contrast with the background color for people with visual impairments. -->
    <div role="article" aria-label="An email from Your Brand Name" lang="en" style="background-color: white; color: #2b2b2b; font-family: 'Avenir Next', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; font-size: 18px; font-weight: 400; line-height: 28px; margin: 0 auto; max-width: 600px; padding: 40px 20px 40px 20px;">

        <!-- Logo section and header. Headers are useful landmark elements. -->
        <header>
            <!-- Since this is a purely decorative image, we can leave the alternative text blank. -->
            <!-- Linking images also helps with Gmail displaying download links next to them. -->
            <a href="https://www.codewof.co.nz/">
                <div style="text-align: center;">
                    <svg width="167.19mm" height="27.155mm" viewBox="0 0 167.19 27.155" xmlns="http://www.w3.org/2000/svg">
                        <g transform="translate(-23.864 -17.383)">
                            <g aria-label="{code:WOF}">
                                <path class="logo_symbol" d="m23.864 28.669h2.2248q0.63357 0 0.97245-0.27995 0.35362-0.29468 0.51569-0.6483 0.17681-0.41256 0.20628-0.94298v-5.2011q0-0.89878 0.33888-1.665 0.33888-0.78091 0.91351-1.3408 0.58936-0.57463 1.3555-0.88405 0.78091-0.32415 1.6502-0.32415h4.2287v4.214h-4.2287v5.2895q0 0.54516-0.10314 1.0019-0.10314 0.45676-0.27995 0.83984-0.17681 0.36835-0.39782 0.67777-0.22101 0.29468-0.45676 0.51569-0.54516 0.54516-1.2377 0.85458 0.6925 0.29468 1.2377 0.86931 0.23574 0.25048 0.45676 0.57463 0.22101 0.32415 0.39782 0.75144 0.17681 0.41255 0.27995 0.94298 0.10314 0.51569 0.10314 1.1493v5.2453h4.2287v4.2287h-4.2287q-0.82511 0-1.606-0.32415-0.76617-0.32415-1.3555-0.89878-0.58936-0.5599-0.94298-1.3408-0.35362-0.76617-0.35362-1.665v-5.2453q0.01473-0.81038-0.25048-1.2524-0.25048-0.44202-0.57463-0.6483-0.38309-0.23575-0.86931-0.27995h-2.2248z"></path>
                                <g class="logo_text">
                                    <path d="m52.08 28.875-2.9468 2.9616q-0.22101-0.61883-0.6041-1.1051-0.38309-0.50096-0.86931-0.83984-0.47149-0.33888-1.0314-0.51569-0.5599-0.17681-1.1493-0.17681-0.82511 0-1.5618 0.33888-0.72197 0.33888-1.2671 0.95772-0.53043 0.6041-0.83984 1.4439t-0.30942 1.8565q0 0.82511 0.30942 1.5471 0.30942 0.72197 0.83984 1.2671 0.54516 0.54516 1.2671 0.85458 0.7367 0.30942 1.5618 0.30942 0.58936 0 1.1345-0.16208 0.54516-0.16208 1.0167-0.45676 0.48622-0.30942 0.85458-0.7367 0.38309-0.44202 0.61883-0.97245l2.9468 2.9616q-0.5599 0.79564-1.2966 1.4292-0.72197 0.63357-1.5765 1.0756-0.83984 0.44202-1.7828 0.66303-0.92825 0.23575-1.9154 0.23575-1.665 0-3.1384-0.61883-1.4587-0.63357-2.5637-1.7239-1.0903-1.0903-1.7239-2.549t-0.63357-3.1236q0-1.8123 0.63357-3.3888t1.7239-2.7405q1.1051-1.1787 2.5637-1.8565 1.4734-0.67777 3.1384-0.67777 0.98718 0 1.9302 0.25048 0.95772 0.25048 1.8123 0.7367 0.86931 0.47149 1.5913 1.164 0.7367 0.6925 1.2671 1.5913z"></path>
                                    <path d="m69.069 33.487q0 1.7681-0.63357 3.3004-0.63357 1.5176-1.7239 2.6374-1.0903 1.1051-2.5637 1.7534-1.4587 0.63357-3.1384 0.63357-1.665 0-3.1384-0.63357-1.4587-0.6483-2.5637-1.7534-1.0903-1.1198-1.7239-2.6374-0.63356-1.5323-0.63356-3.3004 0-1.7976 0.63356-3.3299 0.63357-1.5323 1.7239-2.6374 1.1051-1.1198 2.5637-1.7534 1.4734-0.63357 3.1384-0.63357 1.6797 0 3.1384 0.6041 1.4734 0.58936 2.5637 1.6944 1.0903 1.0903 1.7239 2.6374 0.63357 1.5323 0.63357 3.4183zm-4.0519 0q0-0.97245-0.32415-1.7534-0.30942-0.79564-0.85458-1.3555-0.54516-0.57463-1.2819-0.86931-0.72197-0.30942-1.5471-0.30942t-1.5618 0.30942q-0.72197 0.29468-1.2671 0.86931-0.53043 0.5599-0.83984 1.3555-0.30942 0.78091-0.30942 1.7534 0 0.91351 0.30942 1.6944 0.30942 0.78091 0.83984 1.3555 0.54516 0.57463 1.2671 0.91351 0.7367 0.32415 1.5618 0.32415t1.5471-0.30942q0.7367-0.30942 1.2819-0.86931 0.54516-0.5599 0.85458-1.3555 0.32415-0.79564 0.32415-1.7534z"></path>
                                    <path d="m86.573 41.517h-0.97245l-1.5618-2.1659q-0.57463 0.51569-1.2229 0.97245-0.63357 0.44202-1.3408 0.78091-0.70724 0.32415-1.4587 0.51569-0.7367 0.19154-1.5029 0.19154-1.665 0-3.1384-0.61883-1.4587-0.63357-2.5637-1.7386-1.0903-1.1198-1.7239-2.6374-0.63357-1.5323-0.63357-3.3299 0-1.7828 0.63357-3.3152 0.63357-1.5323 1.7239-2.6521 1.1051-1.1198 2.5637-1.7534 1.4734-0.63357 3.1384-0.63357 0.53043 0 1.0903 0.0884 0.57463 0.08841 1.1051 0.29468 0.54516 0.19154 1.0167 0.51569t0.79564 0.79564v-7.367h4.0519zm-4.0519-8.0301q0-0.82511-0.32415-1.5913-0.30942-0.78091-0.85458-1.3703-0.54516-0.6041-1.2819-0.95772-0.72197-0.36835-1.5471-0.36835t-1.5618 0.29468q-0.72197 0.29468-1.2671 0.85458-0.53043 0.54516-0.83984 1.3408t-0.30942 1.7976q0 0.86931 0.30942 1.6502t0.83984 1.3703q0.54516 0.58936 1.2671 0.92825 0.7367 0.33888 1.5618 0.33888t1.5471-0.35362q0.7367-0.36835 1.2819-0.95772 0.54516-0.6041 0.85458-1.3703 0.32415-0.78091 0.32415-1.606z"></path>
                                    <path d="m95.929 37.657q0.23575 0.07367 0.47149 0.10314 0.23575 0.01473 0.47149 0.01473 0.58936 0 1.1345-0.16208 0.54516-0.16208 1.0167-0.45676 0.48622-0.30942 0.85458-0.7367 0.38308-0.44202 0.61883-0.97245l2.9468 2.9616q-0.5599 0.79564-1.2966 1.4292-0.72197 0.63357-1.5766 1.0756-0.83984 0.44202-1.7828 0.66303-0.92825 0.23575-1.9154 0.23575-1.665 0-3.1384-0.61883-1.4587-0.61883-2.5637-1.7239-1.0903-1.1051-1.7239-2.6227-0.63357-1.5323-0.63357-3.3594 0-1.8712 0.63357-3.4183t1.7239-2.6374q1.1051-1.0903 2.5637-1.6944 1.4734-0.6041 3.1384-0.6041 0.98718 0 1.9302 0.23574 0.94298 0.23575 1.7828 0.67777 0.85458 0.44202 1.5913 1.0903 0.7367 0.63357 1.2966 1.4292zm2.0628-8.2953q-0.27995-0.10314-0.5599-0.13261-0.26521-0.02947-0.5599-0.02947-0.82511 0-1.5618 0.30942-0.72197 0.29468-1.2671 0.85458-0.53043 0.5599-0.83984 1.3555-0.30942 0.78091-0.30942 1.7681 0 0.22101 0.01473 0.50096 0.02947 0.27995 0.07367 0.57463 0.05894 0.27995 0.13261 0.54516t0.19154 0.47149z"></path>
                                </g>
                                <path class="logo_symbol" d="m111.07 29.511q0 0.53043-0.20628 1.0019-0.19154 0.45676-0.53043 0.79564-0.33888 0.33888-0.79564 0.54516-0.45676 0.19154-0.97245 0.19154-0.53043 0-0.98718-0.19154-0.45676-0.20628-0.81038-0.54516-0.33888-0.33888-0.54516-0.79564-0.19154-0.47149-0.19154-1.0019 0-0.50096 0.19154-0.95772 0.20628-0.45676 0.54516-0.79564 0.35362-0.35362 0.81038-0.54516 0.45675-0.20628 0.98718-0.20628 0.51569 0 0.97245 0.20628 0.45676 0.19154 0.79564 0.54516 0.33889 0.33888 0.53043 0.79564 0.20628 0.45676 0.20628 0.95772zm0 8.4574q0 0.53043-0.20628 1.0019-0.19154 0.45676-0.53043 0.79564-0.33888 0.33888-0.79564 0.53043-0.45676 0.20628-0.97245 0.20628-0.53043 0-0.98718-0.20628-0.45676-0.19154-0.81038-0.53043-0.33888-0.33888-0.54516-0.79564-0.19154-0.47149-0.19154-1.0019 0-0.51569 0.19154-0.97245 0.20628-0.45676 0.54516-0.79564 0.35362-0.33888 0.81038-0.53043 0.45675-0.20628 0.98718-0.20628 0.51569 0 0.97245 0.20628 0.45676 0.19154 0.79564 0.53043 0.33889 0.33888 0.53043 0.79564 0.20628 0.45676 0.20628 0.97245z"></path>
                                <g class="logo_text">
                                    <path d="m135.27 35.476q0 1.3113-0.50096 2.4753-0.48623 1.1493-1.3555 2.0186-0.85458 0.85458-2.0186 1.3555-1.1493 0.48622-2.4606 0.48622-1.1787 0-2.269-0.41256-1.0756-0.41255-1.9449-1.2082-0.86931 0.79564-1.9596 1.2082-1.0903 0.41256-2.269 0.41256-1.3113 0-2.4753-0.48622-1.1492-0.50096-2.0186-1.3555-0.85457-0.86931-1.3555-2.0186-0.48623-1.164-0.48623-2.4753v-15.088h4.2287v15.088q0 0.44202 0.16207 0.83984 0.16208 0.38309 0.44203 0.67777 0.29468 0.27995 0.67776 0.44202 0.38309 0.16208 0.82511 0.16208 0.44203 0 0.82511-0.16208 0.38309-0.16208 0.66304-0.44202 0.29468-0.29468 0.45675-0.67777 0.16208-0.39782 0.16208-0.83984v-15.088h4.2287v15.088q0 0.44202 0.16208 0.83984 0.16207 0.38309 0.44202 0.67777 0.29468 0.27995 0.67777 0.44202 0.38308 0.16208 0.82511 0.16208 0.44202 0 0.82511-0.16208 0.38308-0.16208 0.66303-0.44202 0.29468-0.29468 0.45676-0.67777 0.17681-0.39782 0.17681-0.83984v-15.088h4.214z"></path>
                                    <path d="m159.76 31.041q0 1.5029-0.39782 2.9026-0.38308 1.385-1.0903 2.6079-0.70724 1.2082-1.7092 2.2101-1.0019 1.0019-2.2101 1.7239-1.2082 0.70724-2.6079 1.0903-1.3997 0.39782-2.9026 0.39782t-2.9026-0.39782q-1.385-0.38309-2.6079-1.0903-1.2082-0.72197-2.2101-1.7239t-1.7239-2.2101q-0.70724-1.2229-1.1051-2.6079-0.38308-1.3997-0.38308-2.9026t0.38308-2.9026q0.39782-1.3997 1.1051-2.6079 0.72197-1.2082 1.7239-2.2101 1.0019-1.0019 2.2101-1.7092 1.2229-0.70724 2.6079-1.0903 1.3997-0.39782 2.9026-0.39782t2.9026 0.39782q1.3997 0.38309 2.6079 1.0903 1.2082 0.70724 2.2101 1.7092 1.0019 1.0019 1.7092 2.2101 0.70724 1.2082 1.0903 2.6079 0.39782 1.3997 0.39782 2.9026zm-4.1992 0q0-1.385-0.53043-2.6079-0.53043-1.2377-1.4439-2.1364-0.89878-0.91351-2.1364-1.4439-1.2229-0.53043-2.6079-0.53043-1.3997 0-2.6227 0.53043t-2.1364 1.4439q-0.91351 0.89878-1.4439 2.1364-0.53043 1.2229-0.53043 2.6079t0.53043 2.6079q0.53043 1.2082 1.4439 2.1217t2.1364 1.4439q1.2229 0.53043 2.6227 0.53043 1.385 0 2.6079-0.53043 1.2377-0.53043 2.1364-1.4439 0.91351-0.91351 1.4439-2.1217 0.53043-1.2229 0.53043-2.6079z"></path>
                                    <path d="m166.74 41.517h-4.2287v-21.129h14.793v4.2287h-10.564v4.2287h6.3357v4.2287h-6.3357z"></path>
                                </g>
                                <path class="logo_symbol" d="m191.05 32.883h-2.2396q-0.48623 0.0442-0.86932 0.27995-0.16207 0.10314-0.32415 0.26521-0.14734 0.14734-0.26521 0.38309-0.11787 0.22101-0.19154 0.53043-0.0589 0.30942-0.0442 0.72197v5.2453q0 0.89878-0.35362 1.665-0.35362 0.78091-0.94298 1.3408-0.58937 0.57463-1.3703 0.89878-0.76617 0.32415-1.5913 0.32415h-4.214v-4.2287h4.214v-5.2453q0-0.63357 0.10314-1.1493 0.10314-0.53043 0.27995-0.94298 0.17681-0.42729 0.39782-0.75144t0.45676-0.57463q0.54516-0.57463 1.2377-0.86931-0.6925-0.30942-1.2377-0.85458-0.23575-0.22101-0.45676-0.51569-0.22101-0.30942-0.39782-0.67777-0.17681-0.38309-0.27995-0.83984t-0.10314-1.0019v-5.2895h-4.214v-4.214h4.214q0.86931 0 1.6355 0.32415 0.7809 0.30942 1.3555 0.88405 0.58937 0.5599 0.92825 1.3408 0.33889 0.76617 0.33889 1.665v5.2011q0.0295 0.53043 0.20627 0.94298 0.16208 0.35362 0.50096 0.6483 0.33889 0.27995 0.98719 0.27995h2.2396z"></path>
                            </g>
                        </g>
                    </svg>
                </div>
            </a>
            <!-- The h1 is the main heading of the document and should come first. -->
            <!-- We can override the default styles inline. -->
            <h1 style="color: #000000; font-size: 32px; font-weight: 800; line-height: 32px; margin: 36px 0;">
                Your friendly reminder
            </h1>
        </header>

        <!-- Main content section. Main is a useful landmark element. -->
        <main>
            <p>
    """
    email_second_half = """
            </p>

            <!-- This link uses descriptive text to inform the user what will happen with the link is tapped. -->
            <!-- It also uses inline styles since some email clients won't render embedded styles from the head. -->
            <a href="https://www.codewof.co.nz/users/dashboard/" style="color: #007bff; text-decoration: underline;">Let's practice!</a>

            <p>
                Thanks,<br>
                The Computer Science Education Research Group
            </p>
        </main>
        <!-- Footer information. Footer is a useful landmark element. -->
        <footer>
            <div style="border-top: 2px solid #eaeaea;">
                <!-- This link uses descriptive text to inform the user what will happen with the link is tapped. -->
                <!-- It also uses inline styles since some email clients won't render embedded styles from the head. -->
                <p style="font-size: 16px; font-weight: 400; line-height: 24px;">
                    You received this email because you opted into reminders. You can <a href="https://www.codewof.co.nz/users/dashboard/" style="color: #007bff; text-decoration: underline;">change your reminder settings here</a>.
                </p>
            </div>
        </footer>

    </div>
    <!--[if (gte mso 9)|(IE)]>
    </td></tr></table>
    <![endif]-->
    </body>
    </html>
    """

    def handle(self, *args, **options):
        """
        Gets the current day of the week, then obtains the list of Users who should get a reminder today. Sends an
        email to each user with a customised message based on recent usage.
        :param args:
        :param options:
        :return:
        """

        today = timezone.now().date()
        weekday = Weekday(today.weekday())

        users_to_email = self.get_users_to_email(weekday)

        for user in users_to_email:
            date_of_last_attempt = Attempt.objects.filter(profile=user.profile).order_by('datetime')[0].datetime.date()
            days_since_last_attempt = (today - date_of_last_attempt).days

            message = self.create_message(days_since_last_attempt)
            html = self.build_email(message)

            send_mail(
                'CodeWOF Reminder',
                None,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=html
            )

    def build_email(self, message):
        """
        Constructs HTML for the email body
        :param message: The string message
        :return: The HTML as a string
        """
        return self.email_first_half + message + self.email_second_half

    def get_users_to_email(self, weekday_num):
        """
        Gets a list of users that have opted to receive a reminder for the inputted day of the week
        :param weekday_num: The day of the week as an int.
        :return: A QuerySet of Users.
        """
        if weekday_num == Weekday.MONDAY:
            users_to_email = User.objects.filter(remind_on_monday=True)
        elif weekday_num == Weekday.TUESDAY:
            users_to_email = User.objects.filter(remind_on_tuesday=True)
        elif weekday_num == Weekday.WEDNESDAY:
            users_to_email = User.objects.filter(remind_on_wednesday=True)
        elif weekday_num == Weekday.THURSDAY:
            users_to_email = User.objects.filter(remind_on_thursday=True)
        elif weekday_num == Weekday.FRIDAY:
            users_to_email = User.objects.filter(remind_on_friday=True)
        elif weekday_num == Weekday.SATURDAY:
            users_to_email = User.objects.filter(remind_on_saturday=True)
        else:
            users_to_email = User.objects.filter(remind_on_sunday=True)
        return users_to_email

    def create_message(self, days_since_last_attempt):
        """
        Returns a unique message based on recent usage.
        :param days_since_last_attempt: The int days since their last attempt.
        :return: a string message.
        """
        if days_since_last_attempt < 7:
            message = "You've been practicing recently. Keep it up!"
        elif days_since_last_attempt > 14:
            message = "You haven't attempted a question in a long time. " \
                      "Try to use CodeWOF regularly to keep your coding skills sharp. " \
                      "If you don't want to use CodeWOF anymore, " \
                      "then click the link at the bottom of this email to stop getting reminders."
        else:
            message = "It's been awhile since your last attempt. " \
                      "Remember to use CodeWOF regularly to keep your coding skills sharp."
        return message
