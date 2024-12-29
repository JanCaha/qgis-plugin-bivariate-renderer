.PHONY: zip

prepare: clean zipfiles

zip: clean zipfiles delete_after_zip

clean:
	py3clean .
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf

zipfiles:
	pb_tool zip

delete_after_zip:
	rm -rf zip_build/BivariateRenderer
	rm zip_build/*README.txt