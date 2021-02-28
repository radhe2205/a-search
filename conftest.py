import pandas as pd
#For Grading
def pytest_sessionfinish(session, exitstatus):
	anum=0
	qnums=2
	casenums=6
	reporter = session.config.pluginmanager.get_plugin('terminalreporter')
	report={}
	points={'test_question1_case1':10,'test_question1_case2':10,'test_question1_case3':7.5,'test_question1_case4':7.5,'test_question1_case5':7.5,'test_question1_case6':7.5,
	'test_question2_case1':10,'test_question2_case2':10,'test_question2_case3':7.5,'test_question2_case4':7.5,'test_question2_case5':7.5,'test_question2_case6':7.5}
	total=0
	try:
		for test in reporter.stats['passed']:
			report[test.location[2]+"_status"]=[test.outcome]
			report[test.location[2]+"_points"]=[points[test.location[2]]]
			total+=points[test.location[2]]
	except KeyError:
		pass
	try:
		for test in reporter.stats['failed']:
			report[test.location[2]+"_status"]=[test.outcome]
			report[test.location[2]+"_points"]=[0]
	except KeyError:
		pass
	report=pd.DataFrame.from_dict(report)
	report.sort_index(axis=1, inplace=True)
	report['Total']=[total]
	report['Late Penalty']=[0]
	report['Total Autograding']=[total]
	report.T.to_csv("autograding_report.csv",header=False)