from leaseslicensing.components.emails.emails import TemplateEmailBase


def send_winner_notification(request, competitive_process):
    email = TemplateEmailBase(
        subject="Winning, Leases and Licence application is ready",
        html_template="leaseslicensing/emails/competitive_processes/send_winner_notification.html",
        # html_template="leaseslicensing/emails/proposals/send_referral_notification.html",
        txt_template="leaseslicensing/emails/competitive_processes/send_winner_notification.txt",
    )

    # TODO: complete logic below

    context = {

    }
    recipients = [competitive_process.winner.email_address,]

    msg = email.send(recipients, context=context)

    # sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    # _log_proposal_email(msg, proposal, sender=sender)
    # if proposal.org_applicant:
    #     _log_org_email(
    #         msg, proposal.org_applicant, referral, sender=sender
    #     )
    # elif proposal.ind_applicant:
    #     _log_user_email(
    #         msg, proposal.ind_applicant, referral, sender=sender
    #     )
