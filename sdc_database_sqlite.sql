--
-- Database: `sdc_database`
--

-- --------------------------------------------------------

--
-- Table structure for table `ahdhc_members`
--

CREATE TABLE ahdhc_members (
  `member_id` int(11) PRIMARY KEY NOT NULL,
  `last_name` text NOT NULL,
  `first_name` text NOT NULL,
  `department_id` int(11) NOT NULL,
  `is_student` tinyint(1) NOT NULL,

  FOREIGN KEY (department_id) REFERENCES department(department_id)
);

-- --------------------------------------------------------

--
-- Table structure for table `audit_trail`
--

CREATE TABLE audit_trail (
  case_id int(11) NOT NULL,
  entry_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (case_id) REFERENCES cases(case_id)
);

-- --------------------------------------------------------

--
-- Table structure for table `cases`
--

CREATE TABLE `cases` (
  `case_id` int(11) PRIMARY KEY NOT NULL,   
  `complaint_date_received` date NOT NULL,
  `complaint_sdc_receipt_deadline` date NOT NULL,
  `initial_report_deadline` date NOT NULL,
  `initial_report_release_date` date NOT NULL,
  `jurisdiction` int(11) NOT NULL,
  `is_adr_ok` tinyint(1) NOT NULL,
  `adr_deadline` date NOT NULL,
  `did_adr_work` tinyint(1) NOT NULL,
  `case_number` varchar(100) NOT NULL,    
  `adhdc_constitution_deadline` date NOT NULL,
  `ahdhc_constitution_date` date NOT NULL,
  `ahdhc_orientation_date` date NOT NULL,
  `summons_issuance_deadline` date NOT NULL,
  `summons_issuance_date` date NOT NULL,
  `summons_service_deadline` date NOT NULL,
  `summons_service_date` date NOT NULL,
  `summons_receipt_deadline` date NOT NULL,
  `summons_receipt_date` date NOT NULL,
  `respondent_answer_deadline` date NOT NULL,
  `respondednt_answer_date` date NOT NULL,
  `ahdhc_preliminary_deliberation_date` date NOT NULL,
  `preliminary_meeting_notice_deadline` date NOT NULL,
  `preliminary_meeting_date` date NOT NULL,
  `preliminary_meeting_report_done` tinyint(1) NOT NULL,
  `preliminary_meeting_report_date_filed` date NOT NULL,
  `case_resolution_deadline` date NOT NULL,
  `final_committee_report_deadline` date NOT NULL,
  `final_committee_report_receipt_date` date NOT NULL,
  `decision_issuance_deadline` date NOT NULL,
  `decision_issuance_date` date NOT NULL,
  `decision_copy_to_chancellor_deadline` date NOT NULL,
  `decision_copy to_chancellor_date` date NOT NULL,
  `decision_receipt_date` date NOT NULL,
  `appeal_deadline` date NOT NULL,
  `appeal_made` tinyint(1) NOT NULL,
  `case_closed` tinyint(1) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `cases_ahdhc_members`
--

CREATE TABLE `cases_ahdhc_members` (
  `case_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,

  FOREIGN KEY (case_id) REFERENCES cases(case_id),
  FOREIGN KEY (member_id) REFERENCES ahdhc_members(member_id)
);

-- --------------------------------------------------------

--
-- Table structure for table `cases_hearings`
--

CREATE TABLE `cases_hearings` (
  `case_id` int(11) NOT NULL,
  `hearing_date` date NOT NULL,

  FOREIGN KEY (case_id) REFERENCES cases(case_id)
);

-- --------------------------------------------------------

--
-- Table structure for table `cases_misconducts_respondents`
--

CREATE TABLE `cases_misconducts_respondents` (
  `case_id` int(11) NOT NULL,
  `misconduct_id` int(11) NOT NULL,
  `misconduct_details` text NOT NULL,
  `respondent_id` int(11) NOT NULL,
  `is_guilty` tinyint(1) NOT NULL,
  `corrective_measure` text NOT NULL,

  FOREIGN KEY (case_id) REFERENCES cases(case_id),
  FOREIGN KEY (misconduct_id) REFERENCES misconducts(misconduct_id),
  FOREIGN KEY (respondent_id) REFERENCES respondents(respondent_id)
);

-- --------------------------------------------------------

--
-- Table structure for table `college`
--

CREATE TABLE `college` (
  `college_id` int(11) PRIMARY KEY NOT NULL,
  `name` text NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

CREATE TABLE `department` (
  `department_id` int(11) PRIMARY KEY NOT NULL,
  `name` text NOT NULL,
  `college_id` int(11) NOT NULL,

  FOREIGN KEY (college_id) REFERENCES college(college_id)
);

-- --------------------------------------------------------

--
-- Table structure for table `misconducts`
--

CREATE TABLE `misconducts` (
  `misconduct_id` int(11) PRIMARY KEY NOT NULL,
  `csc_section` int(11) NOT NULL,
  `misconduct_general` varchar(100) NOT NULL,
  `misconduct_specific` text NOT NULL,
  `for_student` text NOT NULL,
  `is_serious` tinyint(1) NOT NULL,
  `csc_version` text NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `respondents`
--

CREATE TABLE `respondents` (
  `respondent_id` int(11) PRIMARY KEY NOT NULL,
  `last_name` text NOT NULL,
  `first_name` text NOT NULL,
  `middle_name` text NOT NULL,
  `degree_program` text NOT NULL,
  `department_id` int(11) NOT NULL,
  `is_student` tinyint(1) NOT NULL,

  FOREIGN KEY (department_id) REFERENCES department(department_id)
);

-- --------------------------------------------------------

--
-- Table structure for table `univ_reps`
--

CREATE TABLE `univ_reps` (
  `rep_id` int(11) PRIMARY KEY NOT NULL,
  `last_name` text NOT NULL,
  `first_name` text NOT NULL,
  `department_id` int(11) NOT NULL,

  FOREIGN KEY (department_id) REFERENCES department(department_id)
);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) PRIMARY KEY NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` text NOT NULL,
  `role_id` int(11) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `users_role`
--

CREATE TABLE `users_role` (
  `role_id` int(11) NOT NULL,
  `role_name` text NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `users_role`
--

CREATE TABLE `announcements` (
  `title` text NOT NULL,
  `description` text NOT NULL,
  `date_posted` date NOT NULL
);

-- --------------------------------------------------------

--
-- Trigger for updating cases (goes to audit log)
--

-- CREATE TRIGGER audit_trail_log AFTER INSERT
-- ON cases
-- BEGIN:
-- 	INSERT INTO audit_trail (case_id, entry_date) VALUES (new.ID, DATETIME('now'));
-- END;

-- --------------------------------------------------------

--