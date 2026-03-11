from setuptools import setup

package_name = 'zed_dual_camera'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pdz',
    maintainer_email='mschmotzr@ethz.ch',
    description='ROS 2 node publishing images from two ZED cameras',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'dual_zed_publisher = zed_dual_camera.zed_dual_image_publisher:main',
        ],
    },
)
