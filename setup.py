from setuptools import find_packages, setup  # type: ignore

setup(
    name='symm',
    version='1.0.0',
    description='Discordのチャンネルの直近の画像をシンメトリー化する',
    description_content_type='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nmn29/SYMM',
    author='nmn29',
    packages=find_packages(),
    python_requires='>=3.0',
    include_package_data=True,
    # license='',
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={'console_scripts': ['symm=symm.main:main']})
