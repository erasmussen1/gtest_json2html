#!/usr/bin/env python3

import sys
import os
import shutil
import glob
import math
import json


# Template parameters:
#   test_navbar                 : The navigation bar.
#   tmpl_test_sidebar           : The sidebar.
#   total_test_result           : HTML for total test results.
#   single_test_result_listing  : HTML for single test result listing.
tmpl_main_html = '''
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
              integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
              crossorigin="anonymous">
    <!-- Icons -->
    <link href="open-iconic/font/css/open-iconic-bootstrap.css" rel="stylesheet">
    <!-- Stacktable CSS ->
    <link href="stacktable/css/stacktable.css" rel="stylesheet">
    <!-- Custom CSS -->
    <link href="css/gtest-report.css" rel="stylesheet">
    <title>Googletest HTML-Report</title>
  </head>
  <body>
    {test_navbar}

    <div class="container-fluid">
      <div class="row">
        <nav class="col-md-4 col-md-mw-230 col-xl-mw-300 bg-light sidebar">
          {test_sidebar}
        </nav>

        <main role="main" class="col col-md-8 col-lg-8 mx-auto pt-3">
          {total_test_result}

          <h4 id="single_test_results">Single Test Results</h4>
          {single_test_result_listing}
        </main>
      </div>
    </div>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
                 integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
                 crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
                integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
                crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
                integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
                crossorigin="anonymous"></script>
    <!-- Stacktable -->
        <script src="stacktable/js/stacktable.js"></script>
    <!-- Custom javascript -->
    <script src="js/gtest-report.js"></script>
  </body>
</html>
'''

# Template parameters:
#   project_name                : Name of the project.
tmpl_test_navbar = '''
<nav class="navbar navbar-dark sticky-top bg-dark">
  <span class="navbar-brand">{project_name}</a>
</nav>
'''

# Template parameters:
#   single_testsuite_links           : HTML code with links to single testsuites.
tmpl_test_sidebar = '''
<h3 class="md-sidebar-header">Content</h3>
<div class="sidebar-sticky">
  <ul class="nav flex-column">
    <li class="nav-item">
      <a class="nav-link" href="#total-test-summary">
        <span class="oi oi-graph"></span>Test Summary
      </a>
    </li>
    <hr/>
    <li>
      <a class="nav-link" href="#single_test_results">
        <span class="oi oi-list"></span>Single Test Results
      </a>
      <ul class="nav flex-column" id="testcase-sidebar-list">
          {single_testsuite_links}
      </ul>
    </li>
    <hr/>
    <li class="nav-item">
      <a class="nav-link">
        <span class="oi oi-tags"></span>Tags
      </a>
      <ul class="nav flex-column">
        <li class="tags-container"></li>
      </ul>
    </li>
  </ul>
</div>
'''

# Template parameters:
#   testsuite_html_id       : html id
#   testsuite_name          : name of the testsuite
tmpl_single_testsuite_link = '''
<small>
    <a class="nav-link" href="#{testsuite_html_id}">
      <span class="oi oi-magnifying-glass"></span>{testsuite_name}
    </a>
</small>
'''

# Template parameters:
#   html_class      : HTML class, one of ['success', 'danger', 'warning']
#   percentage_rate : The percentage rate.
#   absolute_value  : The absolute value.
tmpl_progress_bar = '''
<div class="progress-bar bg-{html_class}"
                role="progressbar"
                style="width: {percentage_rate}%"
                aria-valuenow="{percentage_rate}"
                aria-valuemin="0"
                aria-valuemax="100">{percentage_rate}% ({absolute_value})
</div>
'''

# Template paramters:
#   report_file_path           : Path to the report file.
#   testsuite_name             : Name of the testsuite
#   total_abs_test_count       : Total number of tests (absolute).
#   total_abs_success_count    : Total number of succeeded tests (absolute).
#   total_abs_fail_count       : Total number of failed tests (absolute).
#   total_abs_disabled_count   : Total number of disabled tests (absolute).
#   html_progress_bars         : HTML code with progress bars to show.
#   total_execution_time       : The execution time of all test suites.
#   test_timestamp             : Timestamp of the test.
#   test_author                : The author of the test.
tmpl_total_test_result = '''
<!-- Total Test Result Begin -->
<div style="margin-bottom:50px;" class="card" id="total-test-summary">
  <h4 class="card-header">Test Summary of {testsuite_name}</h4>
  <div class="card-body">
    <div class="row">
      <div class="col-12">
        <div class="progress" style="margin-bottom: 20px; height: 20px;">
          {html_progress_bars}
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-12 col-xl-4">
        <p class="font-weight-bold">Report file:</p>
        <p>{report_file_path}</p>
      </div>
      <div class="col-md-auto">
        <p class="font-weight-bold">Tests:</p>
        <p class="text-primary">{total_abs_test_count}</p>
      </div>
      <div class="col-md-auto">
        <p class="font-weight-bold">Fails:</p>
        <p class="text-danger">{total_abs_fail_count}</p>
      </div>
      <div class="col-md-auto">
        <p class="font-weight-bold">Disabled:</p>
        <p class="text-warning">{total_abs_disabled_count}</p>
      </div>
      <div class="col-md-auto">
        <p class="font-weight-bold">Execution time:</p>
        <p>{total_execution_time} sec</p>
      </div>
      <div class="col-md-auto">
        <p class="font-weight-bold">Timestamp:</p>
        <p>{test_timestamp}</p>
      </div>
    </div>
    <div class="row">
        <div class="col-12">
            <small class="text-secondary">Test author: {test_author}</small>
        </div>
    </div>
  </div>
</div>
<!-- Total Test Result End -->
'''

# Template paramters:
#   html_progress_bars             : HTML code with progress bars to show.
#   testsuite_name                 : Name of the testsuite.
#   testsuite_tags                 : Tags for this testsuite.
#   testsuite_html_id              : ID to create site links.
#   testsuite_abs_test_count       : Count of all tests of this testsuite (absolute).
#   testsuite_abs_fails_count      : Count of all fails of this testsuite (absolute).
#   testsuite_abs_disabled_count   : Count of all disabled tests of this testsuite (absolute).
#   testsuite_execution_time       : Execution time of the testsuite.
#   html_single_test_rows          : The html code with table rows for each test.
tmpl_single_test_result_listing = '''
<!-- Single Test Result Listing Begin -->
<div id="{testsuite_html_id}" class="card single-testsuite-container"
       style="margin-top:20px; margin-bottom: 60px;" data-tags="{testsuite_tags}">
  <h5 class="card-header">Testsuite: {testsuite_name}</h5>
  <div class="card-body">
    <div class="single-test-summary">
      <h5 class="font-weight-bold">Summary:</h5>
      <div class="row">
        <div class="col-12">
          <div class="progress" style="margin-bottom: 20px; height: 20px;">
            {html_progress_bars}
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-sm-auto">
          <p class="font-weight-bold">Tests:</p>
          <p class="text-primary">{testsuite_abs_test_count}</p>
        </div>
        <div class="col-sm-auto">
          <p class="font-weight-bold">Fails:</p>
          <p class="text-danger">{testsuite_abs_fails_count}</p>
        </div>
        <div class="col-sm-auto">
          <p class="font-weight-bold">Disabled:</p>
          <p class="text-warning">{testsuite_abs_disabled_count}</p>
        </div>
        <div class="col-sm-auto">
          <p class="font-weight-bold">Execution time:</p>
          <p>{testsuite_execution_time} sec</p>
        </div>
      </div>
      <hr/>
    </div>
    <h5 class="font-weight-bold">Testcases:</h5>
    <div class="container">
      <div class="table-responsive">
        <table class="testcase-table table table-bordered">
          <thead class="testcase-header">
            <tr class="table-active text-center testcase-header-row">
              <th scope="col" class="testcase-header-id">#</th>
              <th scope="col" class="testcase-header-name">Name</th>
              <th scope="col" class="testcase-header-time">Time (sec)</th>
              <th scope="col" class="textcase-header-status">Status</th>
            </tr>
          </thead>
          <tbody>
            {html_single_test_rows}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
<!-- Single Test Result Listing End -->
'''

# Template paramters:
#   test_number                : Number of the test.
#   test_classname             : The classname of the test.
#   test_name                  : Name of the test.
#   test_tags                  : Tags for this testcase.
#   test_execution_time        : Execution time of the test.
#   test_html_class            : The HTML class to colorize the row ['success', 'danger', 'warning']
#   test_icon_name             : Name of the icon to use ['check', 'x', 'warning']
#   html_error_message_list    : HTML code with error message list.
tmpl_single_test_row = '''
<!-- Single Test Row Begin -->
<tr class="table-{test_html_class} testcase-row" data-tags="{test_tags}">
  <th class="text-center testcase-id" scope="row">{test_number}</th>
  <td class="testcase-name">
    {test_classname}::{test_name}<span class="testcase-badges"></span><br>
    {html_error_message_list}
  </td>
  <td class="text-right testcase-time">{test_execution_time}</td>
  <td class="text-center testcase-icon"><span class="oi oi-{test_icon_name}"/></td>
</tr>
<!-- Single Test Row End -->
'''

# Template parameters:
#   html_error_message_items : HTML code with list items
tmpl_error_message_listing = '''
<!-- Error Message Listing Begin -->
<small>
  <ul style="margin-top: 10px;">
    {html_error_message_items}
  </ul>
</small>
<!-- Error Message Listing End -->
'''

# Template parameters:
#   error_message : The error message
#   error_type    : Error type. Leave empty if type is empty.
tmpl_error_message_item = '''
<li><pre>{error_message} {error_type}</pre></li>
'''

usageText = '''

Usage:
    python3 gtest_json2html.py <GTEST_JSON_REPORT_FILE> <OUTPUT_FILE>

    Arguments:
        GTEST_JSON_REPORT_FILE: googletest json report.
        OUTPUT_FILE: Path to the output file, e.g. "output/index.html"

'''


def error_gen(actual, rounded):
    divisor = math.sqrt(1.0 if actual < 1.0 else actual)
    return abs(rounded - actual) ** 2 / divisor


def round_to_100(percents):
    if not math.isclose(sum(percents), 100):
        raise ValueError

    n = len(percents)
    rounded = [int(x) for x in percents]
    up_count = 100 - sum(rounded)
    errors = [(error_gen(percents[i], rounded[i] + 1) - error_gen(percents[i], rounded[i]), i)
              for i in range(n)]

    rank = sorted(errors)
    for i in range(up_count):
        rounded[rank[i][1]] += 1
    return rounded


def generate_progress_bars(abs_total, abs_success, abs_fail, abs_disabled):
    html_progressbars = ''
    if abs_total > 0:
        html_class_list = ['success', 'danger', 'warning']
        abs_value_list = [abs_success, abs_fail, abs_disabled]
        percentage_list = list(
            map(lambda x: 100.0 * x / float(abs_total), abs_value_list))

        rounded_percentage_list = round_to_100(percentage_list)

        for idx in range(len(abs_value_list)):
            abs_value = abs_value_list[idx]
            percentage_rate = rounded_percentage_list[idx]
            html_class = html_class_list[idx]

            if abs_value == 0:
                continue

            html_progressbars += tmpl_progress_bar.format(
                html_class=html_class,
                percentage_rate=percentage_rate,
                absolute_value=abs_value
            )
    else:
        html_progressbars = tmpl_progress_bar.format(
            html_class='success',
            percentage_rate=100,
            absolute_value=0
        )

    return html_progressbars


def get_int(node, lab, default):
    return node[lab] if (lab in node) else 0


def get_str(node, lab, default):
    return node[lab] if (lab in node) else default


def generate_nav_bar(testsuites_node):
    test_project_name = get_str(testsuites_node, 'project', 'Project')

    # Generate HTML for the navigation bar.
    return tmpl_test_navbar.format(
        project_name=test_project_name
    )


def generate_total_test_summary(testsuites_node):
    total_abs_test_count = get_int(testsuites_node, 'tests', 0)
    total_abs_fail_count = get_int(testsuites_node, 'failures', 0)
    total_abs_disabled_count = get_int(testsuites_node, 'disabled', 0)
    total_execution_time = get_str(testsuites_node, 'time', '')
    test_timestamp = get_str(testsuites_node, 'timestamp', '')
    testsuite_name = get_str(testsuites_node, 'name', 'undefined')
    test_author = get_str(testsuites_node, 'author', 'undefined')

    total_abs_success_count = total_abs_test_count - total_abs_fail_count - total_abs_disabled_count

    # Generate HTML for the prograss bar for the test summary.
    total_test_result_progressbars = generate_progress_bars(
        abs_total=total_abs_test_count,
        abs_success=total_abs_success_count,
        abs_fail=total_abs_fail_count,
        abs_disabled=total_abs_disabled_count
    )

    # Generate HTML for the test summary.
    total_test_result = tmpl_total_test_result.format(
        report_file_path=report_filename,
        testsuite_name=testsuite_name,
        total_abs_test_count=total_abs_test_count,
        total_abs_success_count=total_abs_success_count,
        total_abs_fail_count=total_abs_fail_count,
        total_abs_disabled_count=total_abs_disabled_count,
        html_progress_bars=total_test_result_progressbars,
        total_execution_time=total_execution_time,
        test_timestamp=test_timestamp,
        test_author=test_author
    )

    return total_test_result_progressbars, total_test_result


def generate_single_testcase_rows(testsuite_node):
    html_single_testcase_rows = ''
    test_name = ''

    if 'testsuite' not in testsuite_node:
        print("Warning: No nodes {!r} found in testsuite element with name.".format('testsuite'))
        # exit(1)

    testcase_nodes = testsuite_node['testsuite']

    for idx, testcase_node in enumerate(testcase_nodes):
        test_number = idx + 1
        test_name = get_str(testcase_node, 'name', '-undefined-')
        test_execution_time = get_str(testcase_node, 'time', '-undefined-')
        test_status = get_str(testcase_node, 'status', '-undefined-')
        test_classname = get_str(testcase_node, 'classname', '-undefined-')
        test_tags = get_str(testcase_node, 'tags', '')

        test_icon_name = ''
        test_html_class = 'primary'
        html_error_message_list = ''

        # Select icon name and html class considering the number of failure-children and the test status.
        if 'failures' not in testcase_node:
            if test_status == 'RUN':
                test_icon_name = 'check'
                test_html_class = 'success'

        if 'failures' in testcase_node:
            failure_nodes = testcase_node['failures']

            if test_status == 'NOTRUN':
                test_icon_name = 'warning'
                test_html_class = 'warning'
            else:
                test_icon_name = 'x'
                test_html_class = 'danger'

            # If failures occurs, generate the listing with error messages.
            if len(failure_nodes) > 0:
                html_error_message_items = ''

            for failure_node in failure_nodes:
                error_message = get_str(failure_node, 'failure', '-undefined-')
                error_type = get_str(failure_node, 'type', '-undefined-')
                error_type = '' if not error_type else ' (type = {})'.format(error_type)

                html_error_message_items += tmpl_error_message_item.format(
                    error_message=error_message,
                    error_type=error_type
                )

                html_error_message_list = tmpl_error_message_listing.format(
                    html_error_message_items=html_error_message_items
                )

        # Create the HTML code for this single test-case.
        html_single_testcase_rows += tmpl_single_test_row.format(
            test_number=test_number,
            test_classname=test_classname,
            test_name=test_name,
            test_tags=test_tags,
            html_error_message_list=html_error_message_list,
            test_execution_time=test_execution_time,
            test_icon_name=test_icon_name,
            test_html_class=test_html_class
        )

    return html_single_testcase_rows


def generate_single_test_result_listings(testsuites_node):
    html_single_test_result_listing = ''
    collected_testsuite_ids = []

    # Generate HTML for the single test result listings.
    testsuite_nodes = testsuites_node['testsuites']

    id_counter = 0
    for testsuite_node in testsuite_nodes:
        testsuite_name = get_str(testsuite_node, 'name', ' ')
        testsuite_abs_test_count = get_int(testsuite_node, 'tests', 0)
        testsuite_abs_fails_count = get_int(testsuite_node, 'failures', 0)
        testsuite_abs_disabled_count = get_int(testsuite_node, 'disabled', 0)
        testsuite_execution_time = get_str(testsuite_node, 'time', '')
        testsuite_tags = get_str(testsuite_node, 'tags', '')

        testsuite_abs_success_count = testsuite_abs_test_count - \
            testsuite_abs_fails_count - testsuite_abs_disabled_count

        # Generate HTML for single test cases.
        html_single_testcase_rows = generate_single_testcase_rows(testsuite_node)

        html_testsuites_progress_bars = generate_progress_bars(
            abs_total=testsuite_abs_test_count,
            abs_success=testsuite_abs_success_count,
            abs_fail=testsuite_abs_fails_count,
            abs_disabled=testsuite_abs_disabled_count
        )

        html_testsuite = tmpl_single_test_result_listing.format(
            html_progress_bars=html_testsuites_progress_bars,
            testsuite_name=testsuite_name,
            testsuite_tags=testsuite_tags,
            testsuite_html_id=id_counter,
            testsuite_abs_test_count=testsuite_abs_test_count,
            testsuite_abs_fails_count=testsuite_abs_fails_count,
            testsuite_abs_disabled_count=testsuite_abs_disabled_count,
            testsuite_execution_time=testsuite_execution_time,
            html_single_test_rows=html_single_testcase_rows
        )

        collected_testsuite_ids.append((testsuite_name, id_counter))
        id_counter += 1

        html_single_test_result_listing += html_testsuite

    return html_single_test_result_listing, collected_testsuite_ids


def generate_test_sidebar(collected_testsuite_ids):
    html_single_testsuite_links = ''

    for name_id_pair in collected_testsuite_ids:
        html_single_testsuite_links += tmpl_single_testsuite_link.format(
                                            testsuite_name=name_id_pair[0],
                                            testsuite_html_id=name_id_pair[1]
                                        )

    html_test_sidebar = tmpl_test_sidebar.format(
        single_testsuite_links=html_single_testsuite_links
    )

    return html_test_sidebar


def generate_html(json_data, destination_file):
    testsuites_node = json_data
    if len(testsuites_node) == 0:
        print('ERR: The json file doesn\'t have a root node.')
        exit(-1)

    test_navbar = generate_nav_bar(testsuites_node)

    html_single_test_result_listing, collected_testsuite_ids = generate_single_test_result_listings(testsuites_node)

    total_test_result_progressbars, total_test_result = generate_total_test_summary(testsuites_node)

    test_sidebar = generate_test_sidebar(collected_testsuite_ids)

    html_code = tmpl_main_html.format(
        test_navbar=test_navbar,
        test_sidebar=test_sidebar,
        total_test_result=total_test_result,
        single_test_result_listing=html_single_test_result_listing
    )

    return html_code


def copy_html_resources(source_directory, html_resources, destination_directory):
    resource_files = glob.glob(os.sep.join([source_directory, html_resources]))

    for rs in resource_files:
        if os.path.isfile(rs):
            shutil.copy(rs, destination_directory)
        else:
            dirname = os.path.split(rs)[-1]

            target = os.sep.join([destination_directory, dirname])

            if os.path.exists(target):
                shutil.rmtree(target)

            shutil.copytree(rs, os.sep.join([destination_directory, dirname]))


def read_json_file(file_path):
    """
    Reads a JSON file and returns the parsed data.

    :param file_path: Path to the JSON file.
    :return: Parsed JSON data.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"ERR: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"ERR: The file {file_path} contains invalid JSON.")
    except Exception as e:
        print(f"ERR: An unexpected error occurred: {e}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(usageText)
        exit(0)

    arg1 = sys.argv[1]
    arg2 = sys.argv[2]

    source_directory = os.path.dirname(os.path.realpath(__file__))
    report_filename = arg1
    report_file = os.path.realpath(arg1)
    destination_file = os.path.realpath(arg2)
    destination_directory = os.path.dirname(arg2)

    if not os.path.exists(report_file):
        print('ERR: The report file {} does not exists.'.format(report_file))
        print(usageText)
        exit(1)

    if not destination_directory:
        print('ERR: Destination directory is empty')
        print(usageText)
        exit(1)

    # Create the destination directory if not exists.
    if not os.path.isdir(destination_directory):
        os.makedirs(destination_directory)

    # Copy files from html_resources.
    copy_html_resources(source_directory, 'html_resources/*', destination_directory)

    # Generate html.
    print('Start generation:')
    print('  input  : {}'.format(report_file))
    print('  output : {}'.format(destination_file))

    json_data = read_json_file(report_file)

    html_code = generate_html(json_data, destination_file)

    with open(destination_file, 'w') as outfile:
        outfile.write(html_code)

    print('Html was generated successful.')
