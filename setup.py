import setuptools

setuptools.setup(
    name='audio-speech-to-sign-language-converter',
    version='0.1.0',
    description='Python project',
    author='Jigar Gajjar',
    author_email='jigargajjar.55jg@gmail.com',
    url='https://github.com/jigargajjar55/Audio-Speech-To-Sign-Language-Converter',
    packages=setuptools.find_packages(),
    install_requires=[
        'asgiref==3.5.2',
        'click==8.1.3',
        'Django>=4.1.9',
        'joblib==1.2.0',
        'nltk==3.7',
        'regex==2022.10.31',
        'sqlparse>=0.4.4',
        'tqdm==4.64.1',
    ],
)
