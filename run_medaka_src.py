import logging
import os
import time

from medaka.medaka import _validate_common_args, medaka_parser

if __name__ == "__main__":
    # Some users report setting this helps them resolve issues on their
    # filesystems.
    os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
    parser = medaka_parser()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)

    DATASET="AP"

    # dump data and performance evaluation
    args = parser.parse_args(
        [
            "inference",
            current_dir + f"/../generated_files/{DATASET}/medaka_consensus_train/calls_to_draft.bam",
            current_dir + f"/../generated_files/{DATASET}/medaka_consensus_train/consensus_probs.hdf",
            "--model",
            "r941_e81_fast_g514",
            # "r941_e81_hac_g514"
            # "r941_e81_sup_g514",
            "--batch_size",
            "50",
            #"--threads",
            #"1",
            #"--full_precision",
            #"--quantization",
            #"3",
        ]
    )


    # # evaluate
    # args = parser.parse_args(
    #     [
    #         "consensus",
    #         current_dir + "/../generated_files/medaka_consensus_train/calls_to_draft.bam",
    #         current_dir + "/../generated_files/medaka_consensus_train/consensus_probs.hdf",
    #         "--model",
    #         current_dir + "/../generated_files/shennung_model_transformer/model-best_val_cat_acc.tar.gz",
    #         "--batch_size",
    #         "25",
    #         "--threads",
    #         "1",
    #         "--full_precision",
    #         "--quantization",
    #         "3",
    #     ]
    # )

    # # quantization
    # args = parser.parse_args(
    #     [
    #         "quantization",
    #         "../medaka_consensus_train/calls_to_draft.bam",
    #         "../medaka_consensus_train/consensus_probs.hdf",
    #         "--model",
    #         "../shennung_model_transformer/model-best_val_cat_acc.tar.gz",
    #         "--batch_size",
    #         "50",
    #         "--threads",
    #         "1",
    #         "--full_precision",
    #         "--quantization",
    #         "2",
    #     ]
    # )

    # # training
    # args = parser.parse_args(
    #     [
    #         "train",
    #         "../train_features.hdf",
    #         "--train_name",
    #         "../shennung_model_transformer",
    #         "--epochs",
    #         "10",
    #         "--batch_size",
    #         "25",
    #         "--quantization",
    #         "2",
    #         "--model",
    #         "../shennung_model_transformer/model-best_val_cat_acc.tar.gz",
    #     ]
    # )

    # # features
    # args = parser.parse_args(
    #     [
    #         "features",
    #         "../generated_files/calls2draft.bam",
    #         "../train_features.hdf",
    #         "--truth",
    #         "../generated_files/truth2draft.bam",
    #         "--threads",
    #         "1",
    #         "--region",
    #         "utg000001c:-3762624",
    #         "--batch_size",
    #         "100",
    #         "--chunk_len",
    #         "1000",
    #         "--chunk_ovlp",
    #         "0",
    #     ]
    # )
    

    # args for tools

    start_time = time.time()

    # tf.profiler.experimental.start("../output/medaka/logdir")

    # with tf.profiler.experimental.Profile("logdir"):
    logging.basicConfig(
        format="[%(asctime)s - %(name)s] %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
    logger = logging.getLogger(__package__)
    logger.setLevel(args.log_level)

    if args.command == "tools" and not hasattr(args, "func"):
        # display help if given `medaka tools (--help)`
        # TODO: is there a cleaner way to access this?
        parser.__dict__["_actions"][1].choices["tools"].print_help()
    else:
        # perform some post processing on the values, then run entry point
        _validate_common_args(args, parser)
        args.func(args)

    # tf.profiler.experimental.stop()

    logger.info("Total runtime: %.2f s", time.time() - start_time)