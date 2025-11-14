#!/usr/bin/env node
import 'source-map-support/register'
import * as cdk from 'aws-cdk-lib'
import { ArchiveSyncScheduledTaskStack } from '../lib/cdk-stack'

// https://docs.aws.amazon.com/cdk/latest/guide/environments.html

const app = new cdk.App()
new ArchiveSyncScheduledTaskStack(app, 'ArchiveSyncScheduledTaskStack', {
  env: { account: '989828836662', region: 'us-west-2' },
})
