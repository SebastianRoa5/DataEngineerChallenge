clean:
	@find . -name '*.db' -type f -delete
	@find . -type d -name 'logs' -exec rm -rf {} +
	@rm -rf ./logs
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -name '*.pid' -type f -delete
	@find . -name '*password.txt' -type f -delete