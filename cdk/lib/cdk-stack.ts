import { Stack, StackProps } from 'aws-cdk-lib'
import { Construct } from 'constructs'
import {
  FlowLogDestination,
  InstanceType,
  NatProvider,
  SubnetType,
  Vpc,
} from 'aws-cdk-lib/aws-ec2'
import {
  Cluster,
  ContainerImage,
  FargatePlatformVersion,
  LogDriver,
} from 'aws-cdk-lib/aws-ecs'
import { ScheduledFargateTask } from 'aws-cdk-lib/aws-ecs-patterns'
import { Schedule } from 'aws-cdk-lib/aws-events'
import { Repository } from 'aws-cdk-lib/aws-ecr'

export class ArchiveSyncScheduledTaskStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props)

    const vpc = new Vpc(this, 'VPC', {
      maxAzs: 1,
      subnetConfiguration: [
        {
          name: 'Public',
          subnetType: SubnetType.PUBLIC,
        },
        {
          name: 'Private',
          subnetType: SubnetType.PRIVATE_WITH_EGRESS,
        },
      ],
      natGatewayProvider: NatProvider.instanceV2({
        instanceType: new InstanceType('t2.nano'),
      }),
      flowLogs: {
        cloudwatchLogs: {
          destination: FlowLogDestination.toCloudWatchLogs(),
        },
      },
    })

    const cluster = new Cluster(this, 'ECSCluster', {
      vpc,
    })

    new ScheduledFargateTask(this, 'ScheduledTask', {
      cluster: cluster,
      platformVersion: FargatePlatformVersion.LATEST,
      desiredTaskCount: 1,
      schedule: Schedule.expression('cron(0 14 * * ? *)'), // Run at 2pm (UTC) every day
      subnetSelection: { subnetType: SubnetType.PRIVATE_WITH_EGRESS },
      scheduledFargateTaskImageOptions: {
        image: ContainerImage.fromEcrRepository(
          Repository.fromRepositoryName(this, 'ECRImage', 'archive-sync')
        ),
        cpu: 256,
        memoryLimitMiB: 512,
        logDriver: LogDriver.awsLogs({
          streamPrefix: 'ArchiveSync_ScheduledTaskLogs',
        }),
      },
    })
  }
}
