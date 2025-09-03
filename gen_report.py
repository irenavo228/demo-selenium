import subprocess
import os


def run_tests_and_generate_report():
    allure_results_dir = "allure-results"
    allure_report_dir = "allure-report"
    if not os.path.exists(allure_results_dir):
        os.makedirs(allure_results_dir)
    print("Running tests and generating allure results...")
    subprocess.run(["pytest", "--alluredir", allure_results_dir], check=True)
    print("Generating allure report...")
    subprocess.run(["allure", "generate", allure_results_dir, "-o", allure_report_dir, "--clean"], check=True)
    print("Opening allure report...")
    subprocess.run(["allure", "open", allure_report_dir], check=True)


if __name__ == "__main__":
    run_tests_and_generate_report()
